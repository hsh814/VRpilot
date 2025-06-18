"""
-------------------------------------------------
   File Name:       rq2
   Description:     VRpilot
   by using GPT-3.5-turbo model
-------------------------------------------------
"""

from main.utils.gpt_util import if_exceed_token_limit
import os
from path_config import DATA_DIR, CONFIG_DIR, PRO_DIR
from main.data_structure.project import Project, extract_err_msg_from_build_log
from main.utils.git_util import get_parent_commit, reset_repo
from main.utils.file_util import read_file, write_file, delete_folder, append_str_to_file
from main.utils.markdown_util import generate_patch_with_GPT_response, generate_patch_with_GPT_response_new, make_patch_with_diff
from main.utils.docker_util import clear_all_docker_containers
from main.utils.json_util import read_json_from_file
from main.utils.time_util import get_current_time
from main.data_structure.vulnerability import Vulnerability
from main.core.interact_with_GPT import interact_with_openai
from main.utils.diff_util import print_diff
from main.core.prompt import prompt_generator


def setup_result_folders(RESULT_DIR, project_name, vul_id, prompt_type):
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    exp_dir = os.path.join(RESULT_DIR, vul_id,
                           project_name+vul_id)
    if not os.path.exists(exp_dir):
        os.makedirs(exp_dir)
    prompt_type_dir = os.path.join(exp_dir, prompt_type)
    if os.path.exists(prompt_type_dir):
        delete_folder(prompt_type_dir)
    os.mkdir(prompt_type_dir)
    os.mkdir(os.path.join(prompt_type_dir, "prompt"))
    os.mkdir(os.path.join(prompt_type_dir, "response"))
    os.mkdir(os.path.join(prompt_type_dir, "patch"))
    os.mkdir(os.path.join(prompt_type_dir, "regressionTest"))
    os.mkdir(os.path.join(prompt_type_dir, "securityTest"))
    os.mkdir(os.path.join(prompt_type_dir, "buildError"))

    return prompt_type_dir


if __name__ == "__main__":

    # parameter setting
    CUR_RQ = "RQ2"
    PROJECT_NAME = "libtiff"
    MODEL_NAME = "gpt-3.5-turbo"  # ["gpt-4-0314", "gpt-3.5-turbo"]
    TEMPERATURES = [0,0.25,0.5,0.75,1]
    REPEAT = 5
    MAX_QUERY_CNT = 5
    BEST_INIT_PROMPT_DICT = {"EF01": "new",
                             #  "EF02_01": "asan-line2line-oracle-nofunction",
                             #  "EF02_02": "asan-line2line-oracle-nomessage",
                             #  "EF07": "asan-line2line-oracle-nomessage-notoken-assymetric",
                             #  "EF08": "asan-line2line-oracle-nomessage",
                             #  "EF09": "asan-line2line-oracle-nomessage-assymetric",
                             #  "EF10": "asan-line2line-oracle-nomessage-assymetric",
                             #  "EF15": "asan-line2line-oracle-nomessage-assymetric",
                             "EF17": "asan-line2line-oracle-nomessage",
                             "EF18": "asan-line2line-oracle-nomessage-notoken-assymetric",
                             #  "EF20": "asan-line2line-oracle-nomessage-assymetric",
                             #  "EF22": "asan-line2line-oracle-nomessage-notoken-assymetric"
                             }
    RESULT_DIR = os.path.join(PRO_DIR, "result", CUR_RQ, )

    # init
    project_dir = os.path.join(
        DATA_DIR, "repos", PROJECT_NAME)
    config_fpath = os.path.join(
        CONFIG_DIR, PROJECT_NAME, "configuration.json")
    repo_dir = os.path.join(project_dir, "repos", PROJECT_NAME)

    # Read configuration from json file
    config_data = read_json_from_file(config_fpath)
    for idx in range(0, len(config_data["configurations"])):

        config = config_data["configurations"][idx]

        vul = Vulnerability()
        vul.init_from_config(config)

        target_commit = get_parent_commit(
            repo_dir, vul.fix_commit)  # vulernable version
        img_tag = "0"  # start with "0"
        reset_repo(repo_dir, target_commit)
        # init
        clear_all_docker_containers()
        # run the test for the original (vulnerable) version
        project = Project(vul.vul_id, PROJECT_NAME,
                          project_dir, target_commit, img_tag)
        vul.set_project(project)
        project.init_env()

        # gatekeeper
        if_success, build_log = project.build()
        if if_success == False:
            print("Build failed, something wrong here!", get_current_time())
            exit(0)

        vul_fun_test_res, vul_sec_test_res = project.run_test()
        print("Vulnerable version reg test result: passed {}: failed {}".format(
            vul_fun_test_res['passed'], vul_fun_test_res['failed']))
        print("Vulnerable version security test result: #if passed? {}".format(
            vul_sec_test_res['if_passed']))

        # gatekeeper
        if vul_sec_test_res['if_passed'] == True:
            print("{} The original version is secure, something wrong here!".format(
                vul.vul_id), get_current_time())
            exit(0)

        # Saves the unique responses
        init_prompt = "new"#BEST_INIT_PROMPT_DICT[vul.vul_id]
        vul_code = read_file(os.path.join(
            vul.project.ori_repo_dir, vul.vul_code_file_rel_path))
        query_idx = 1
        outputs = []
        unique = 0
        compilable = 0
        plausible = 0
        functional = 0
        vulnerable = 0
        total = 0

        without_feedback_compilable = 0
        witout_feedback_plausible = 0

        clear_all_docker_containers()
        # Create result folder and saves response, prompt there
        cur_prompt_type_dir = setup_result_folders(
            RESULT_DIR, PROJECT_NAME, vul.vul_id, init_prompt)

        res_path = os.path.join(cur_prompt_type_dir, "result.txt")
        if os.path.exists(res_path):
            print("Result {} already exists".format(
                PROJECT_NAME+vul.vul_id+"-"+init_prompt))
            continue
        res_content = ""
        # iterate through the 5 temperatures
        for temper in TEMPERATURES:
            # Initialize the conversation history
            conversation_history = ""
            LOG_PREFIX = "### RQ:{}\n\n### Project:{}\n\n### Case:{}\n\n### Prompt Type:{}\n\n".format(
                CUR_RQ, PROJECT_NAME, vul.vul_id, init_prompt)

            # repeat 10 times
            for repeat_idx in range(0, REPEAT):

                cur_conversation_history = ""
                cur_compile_err_msg = None
                cur_fun_err_msg = []
                cur_sec_err_msg = None
                cur_changed_line_cnt = None
                cur_change = None

                cur_compilable = 0
                cur_plausible = 0
                total = total + 1

                cur_log_fpath = os.path.join(
                    cur_prompt_type_dir, "temp_"+str(
                        temper)+"_itr_"+str(repeat_idx)+"-log.txt")
                append_str_to_file(LOG_PREFIX, cur_log_fpath)

                # query at most 5 times
                for query_idx in range(1, MAX_QUERY_CNT + 1):
                    print("[Timer]: {} Start - Prompt #{}, temperature {}, repeat_idx #{}, query_idx #{},{}".format(
                        vul.vul_id, init_prompt, temper, repeat_idx, query_idx, get_current_time()))

                    prompt, initial_code = prompt_generator(
                        query_idx, repo_dir, config, init_prompt, vul, compile_err_msg=cur_compile_err_msg, fun_err_msg=cur_fun_err_msg, sec_err_msg=cur_sec_err_msg, prompt_dir=cur_prompt_type_dir, cur_change=cur_change)
                    prompt = f"{cur_conversation_history}\n{prompt}".strip()
                    append_str_to_file(
                        "### Query #{} Prompt:\n{}\n\n".format(query_idx, prompt), cur_log_fpath)

                    if_exceed, num_of_tokens = if_exceed_token_limit(
                        prompt, MODEL_NAME)
                    if if_exceed:
                        print("Exceed token limit")
                        append_str_to_file("### Query #{} ends because of Exceed token limit.\n".format(
                            query_idx), cur_log_fpath)
                        if (cur_compilable > 0):
                            compilable = compilable + 1
                        if (cur_plausible > 0):
                            plausible = plausible + 1
                        break

                    append_str_to_file("### Query #{} Prompt Length (Tokens): {}\n\n".format(query_idx,
                        num_of_tokens), cur_log_fpath)

                    print("[Timer] {} Start to get Response from ChatGPT, {}".format(
                        vul.vul_id, get_current_time()))
                
                    model_response = interact_with_openai(MODEL_NAME, prompt, temper)

                    ###########ZERO SHOT CoT
                    prompt += "\n" + model_response + "\n Therefore the fixed code is\n" + initial_code
                    model_response = interact_with_openai(MODEL_NAME, prompt, temper)

                    print("[Timer] {} End to get Response from ChatGPT, {}".format(
                        vul.vul_id, get_current_time()))

                    append_str_to_file("### Query #{} Model Response: {}\n\n".format(query_idx,
                        model_response), cur_log_fpath)

                    if model_response == None:
                        append_str_to_file("### Query #{} ends because of model response is None.\n".format(
                            query_idx), cur_log_fpath)
                        continue

                    # Saving the prompt in a file
                    path_prompt = os.path.join(cur_prompt_type_dir, "prompt", "temp_"+str(
                        temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"_prompt.txt")
                    write_file(path_prompt, prompt, create_dir=True)

                    # Saving the response in a file
                    path_response = os.path.join(cur_prompt_type_dir, "response", "temp_"+str(
                        temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"_response.txt")
                    write_file(path_response, model_response, create_dir=True)
                    #continue
                    # Check if the model's response is valid
                    img_tag = (str)(((int)(img_tag) + 1) % 100)
                    project = Project(vul.vul_id, PROJECT_NAME,
                                      project_dir, target_commit, img_tag)
                    project.init_env()
                    patch, modified_code = make_patch_with_diff(
                        config_fpath, project, model_response, idx)
                    #continue
                    append_str_to_file("### Query #{} Modified_code:{}\n\n".format(query_idx,
                        modified_code), cur_log_fpath)
                    patch_path = os.path.join(cur_prompt_type_dir, "patch", "temp_"+str(
                        temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+vul.vul_code_file)
                    write_file(patch_path, patch, create_dir=True)

                    diff_str, cur_changed_line_cnt = print_diff(
                        vul_code.split('\n'), patch.split('\n'))
                    append_str_to_file(
                        "### Query #{} Diff:\n{}\n\n".format(query_idx, diff_str), cur_log_fpath)

                    # inject the model's response into project
                    project.inject_patch(vul.vul_code_file_rel_path, patch)
                    if_build_sucess, build_log = project.build()

                    if if_build_sucess == False:  # if patch is NOT compilable
                        print("image build faild")
                        cur_compile_err_msg = extract_err_msg_from_build_log(
                            vul.vul_code_file_rel_path, build_log, vul.vul_code_block_start_line, vul.vul_code_block_end_line)
                        path_build_log = os.path.join(cur_prompt_type_dir, "buildError", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"buildLog.txt")
                        write_file(path_build_log, build_log, create_dir=True)
                        reject_path = os.path.join(cur_prompt_type_dir, "response", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"_response_reject.txt")
                        os.rename(path_response, reject_path)
                        append_str_to_file("### Query #{} ends because of model response is not compilable. Build log:\n{}\n\n".format(
                            query_idx, cur_compile_err_msg), cur_log_fpath)
                        cur_fun_err_msg = []
                        cur_sec_err_msg = None

                    else:
                        cur_compile_err_msg = None
                        if (query_idx == 1):
                            without_feedback_compilable += 1
                        cur_compilable = cur_compilable + 1
                        cur_fun_test_res, cur_sec_test_res = project.run_test()

                        path_regression_log = os.path.join(
                            cur_prompt_type_dir, "regressionTest", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"regressionLog.txt")
                        write_file(path_regression_log,
                                   cur_fun_test_res["log"], create_dir=True)

                        path_security_log = os.path.join(
                            cur_prompt_type_dir, "securityTest", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"securityLog.txt")
                        write_file(path_security_log,
                                   cur_sec_test_res["log"], create_dir=True)

                        if ((cur_fun_test_res["failed"] == 0) and cur_sec_test_res['if_passed']):
                            res_content = res_content + \
                                f"Correct response found for {vul.vul_id} at temperature {temper}, iteration {repeat_idx}, query idx {query_idx}\n"
                            # write_file(res_path, res_content, create_dir=True)
                            print("Correct response found at query idx: ", query_idx)
                            if (query_idx == 1):
                                witout_feedback_plausible += 1

                            cur_plausible = cur_plausible + 1
                            # if (cur_compilable > 0):
                            #     compilable = compilable + 1
                            # if (cur_plausible > 0):
                            #     plausible = plausible + 1

                            append_str_to_file("### Query #{} ends because correct response has been found.\n\n".format(
                                query_idx), cur_log_fpath)
                            break

                        if (cur_fun_test_res["failed"] > 0 ):
                            failed_path = os.path.join(cur_prompt_type_dir, "response", "temp_"+str(temper)+"_itr_"+str(
                                repeat_idx)+"_query_"+str(query_idx)+"_response_failed_regression.txt")
                            write_file(failed_path, model_response,
                                       create_dir=True)
                            for test_case in cur_fun_test_res["error_msg"]:
                                cur_fun_err_msg.append(test_case)

                        if cur_sec_test_res['if_passed'] == False:
                            cur_sec_err_msg = cur_sec_test_res['error message']
                            sec_failed_path = os.path.join(cur_prompt_type_dir, "response", "temp_"+str(
                                temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"_response_failed_security.txt")
                            os.rename(path_response, sec_failed_path)

                    # Update the conversation history for next interaction
                    # cur_conversation_history += f"{prompt}\n"
                    # cur_conversation_history += f"The following are the code changes you suggested: {diff_str}\n"
                    cur_change = diff_str

                if (cur_compilable > 0):
                    compilable = compilable + 1
                if (cur_plausible > 0):
                    plausible = plausible + 1
                append_str_to_file("Total: {}\nCompilable: {}\nPlausible: {}\nWithout feedback compilable: {}\nWithout feedback plausible: {}".format(total, compilable, plausible, without_feedback_compilable, witout_feedback_plausible), cur_log_fpath)
        res_content = res_content + "Total: " + str(total)+'\n'+"Compilable: " + str(compilable)+'\n'+"plausible: " + str(
            plausible)+'\n' + "Without feedback compilable: "+str(without_feedback_compilable)+"\n" + "Without feedback plausible: " + str(witout_feedback_plausible)+"\n"
        write_file(res_path, res_content, create_dir=True)
        print(res_content)
