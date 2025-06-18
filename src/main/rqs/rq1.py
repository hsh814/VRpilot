"""
-------------------------------------------------
   File Name:       rq1
   Description:     Compare with Zero-shot paper
   by using GPT-3.5-turbo model
-------------------------------------------------
"""

from main.utils.gpt_util import if_exceed_token_limit
import os
from path_config import DATA_DIR, CONFIG_DIR, PRO_DIR
from main.data_structure.project import Project
from main.utils.git_util import get_parent_commit, reset_repo
from main.utils.file_util import write_file, delete_folder, read_file
from main.utils.markdown_util import generate_patch_with_GPT_response, getFuncBlock, generate_patch_with_GPT_response1
from main.utils.docker_util import clear_all_docker_containers
from main.utils.json_util import read_json_from_file
import time
from main.utils.time_util import get_current_time
from main.data_structure.vulnerability import Vulnerability
from main.core.interact_with_GPT import interact_with_openai
from main.utils.code_util import format_c_code
from main.utils.diff_util import print_diff
from main.core.prompt import prompt_generator



def setup_result_folders(project_name, vul_id, prompt_type):
    if not os.path.exists(RESULT_DIR):
        os.mkdir(RESULT_DIR)
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
    CUR_RQ = "RQ1"
    PROJECT_NAME = "libtiff"
    MODEL_NAME = "gpt-3.5-turbo"  # ["gpt-4-0314", "gpt-3.5-turbo"]
    TEMPERATURES = [0, 0.25, 0.5, 0.75, 1]
    REPEAT = 10
    PROMPT_TYPE = ["asan-line2line-oracle-nofunction", "asan-line2line-oracle-nomessage", "asan-line2line-oracle-nomessage-assymetric",
                   "asan-line2line-oracle-nomessage-notoken-assymetric", "asan-line2line-oracle-simple-prompt-1", "asan-line2line-oracle-simple-prompt-2", "new"]
    PROMPT_DIR = os.path.join(PRO_DIR, CUR_RQ, "prompt")
    RESULT_DIR = os.path.join(PRO_DIR, CUR_RQ, "result")

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

        # print(vul_id, fix_commit, vul_code_file_rel_path,
        #       vul_code_block_start_line, vul_code_block_end_line, vul_description)
        print("[Timer]: {} Start - init,{}".format(vul.vul_id, get_current_time()))

        target_commit = get_parent_commit(
            repo_dir, vul.fix_commit)  # vulernable version
        img_tag = "0"  # start with "0"
        reset_repo(repo_dir, target_commit)
        # init
        clear_all_docker_containers()
        # run the test for the original (vulnerable) version
        project = Project(vul.vul_id, PROJECT_NAME,
                          project_dir, target_commit, img_tag)
        project.init_env()
        vul.set_project(project)

        # gatekeeper
        if_build_sucess, build_error_msg = project.build()
        if if_build_sucess == False:
            print("Build failed, something wrong here!", get_current_time())
            exit(0)
        
        vul_fun_test_res, vul_sec_test_res = project.run_test()
        print("Vulnerable version reg test result: passed #{}, failed #{}".format(
            vul_fun_test_res["passed"], vul_fun_test_res["failed"]))
        print("Vulnerable version security test result: {}".format(vul_sec_test_res["if_passed"]))

        # gatekeeper
        if vul_sec_test_res == True:
            print("{} The original version is secure, something wrong here!".format(
                vul.vul_id), get_current_time())
            exit(0)
        #exit(0)
        # Initialize the conversation history
        conversation_history = ""

        print("[Timer]: {} End - init, {}".format(vul.vul_id, get_current_time()))
        # iterate through the 6 prompts
        #for prompt_idx in range(0, len(PROMPT_TYPE)):
        for prompt_idx in range(2, 3):
            print("[Timer]: {} Start - Prompt #{},{}".format(vul.vul_id,
                  prompt_idx, get_current_time()))

            # Saves the unique responses
            cur_prompt = PROMPT_TYPE[prompt_idx]

            # if cur_prompt != "new":
            #     continue

            outputs = []
            unique = 0
            compilable = 0
            plausible = 0
            functional = 0
            vulnerable = 0
            total = 0
            prev_temper = 0

            res_path = os.path.join(
                RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "result.txt")
            if os.path.exists(res_path):
                print("Result {} already exists".format(
                    PROJECT_NAME+vul.vul_id+"-"+cur_prompt))
                continue

            clear_all_docker_containers()
            # Create result folder and saves response, prompt there
            cur_prompt_type_dir = setup_result_folders(PROJECT_NAME, vul.vul_id,
                                 cur_prompt)
            # iterate through the 5 temperatures
            for temper in TEMPERATURES:

                print("[Timer]: {} Start - Prompt #{}, temperature {}, {}".format(
                    vul.vul_id, prompt_idx, temper, get_current_time()))

                for repeat_idx in range(0, REPEAT):

                    print("[Timer]: {} Start - Prompt #{}, temperature {}, repeat_idx #{}, {}".format(
                        vul.vul_id, prompt_idx, temper, repeat_idx, get_current_time()))

                    if (prev_temper != temper):
                        time.sleep(1)
                    prev_temper = temper
                    prompt, initial_block = prompt_generator(1,
                        repo_dir, config, cur_prompt, vul, prompt_dir= PROMPT_DIR)
                    prompt = f"{conversation_history}\n{prompt}".strip()
                    #print(prompt)

                    if_exceed, num_of_tokens = if_exceed_token_limit(prompt, MODEL_NAME)
                    if if_exceed:
                        break
                    # Get the model's response
                    print("[Timer] {} Start to get Response from ChatGPT, {}".format(
                        vul.vul_id, get_current_time()))
                    model_response = interact_with_openai(
                        MODEL_NAME, prompt, temper)
                    
                    print("[Timer] {} End to get Response from ChatGPT, {}".format(
                        vul.vul_id, get_current_time()))

                    total = total + 1

                    # Saving the prompt in a file
                    path_prompt = os.path.join(
                        RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "prompt", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"_prompt.txt")
                    write_file(path_prompt, prompt, create_dir=True)

                    # Saving the response in a file
                    path_response = os.path.join(
                        RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "response", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"_response.txt")
                    write_file(path_response, model_response, create_dir=True)
                    reject_path = os.path.join(
                        RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "response", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"_response_reject.txt")
                    #exit(0)
                    # Check if the model's response is valid
                    img_tag = (str)(((int)(img_tag) + 1) % 100)
                    project = Project(vul.vul_id, PROJECT_NAME,
                                      project_dir, target_commit, img_tag)
                    project.init_env()
                    patch, modified_code = generate_patch_with_GPT_response1(
                        config_fpath, project, model_response, idx)
                    patch_path = os.path.join(
                        RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "patch", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+vul.vul_code_file)
                    write_file(patch_path, patch, create_dir=True)
                    if (patch == ""):
                        print("Unable to generate", get_current_time())
                        os.rename(path_response, reject_path)
                        continue

                    diff_str, cur_changed_line_cnt = print_diff(
                        format_c_code(vul.vul_code_fun).split('\n'), format_c_code(patch).split("\n"))

                    # inject the model's response into project
                    project.inject_patch(vul.vul_code_file_rel_path, patch)
                    if_build_sucess, build_error_msg = project.build()
                    if if_build_sucess == False:
                        os.rename(path_response, reject_path)
                        path_build_log = os.path.join(cur_prompt_type_dir, "buildError", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"buildLog.txt")
                        write_file(path_build_log, build_error_msg, create_dir=True)
                        continue

                    compilable = compilable + 1
                    cur_fun_test_res, cur_sec_test_res = project.run_test()

                    path_regression_log = os.path.join(
                            cur_prompt_type_dir, "regressionTest", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"regressionLog.txt")
                    write_file(path_regression_log,
                                   cur_fun_test_res["log"], create_dir=True)

                    path_security_log = os.path.join(
                            cur_prompt_type_dir, "securityTest", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"securityLog.txt")
                    write_file(path_security_log,
                                   cur_sec_test_res["log"], create_dir=True)

                    if vul_fun_test_res['passed'] <= cur_fun_test_res['passed']:
                        functional = functional + 1
                        if cur_sec_test_res['if_passed'] == True:
                            print("Correct patch found!")
                            plausible = plausible + 1
                            func_block = getFuncBlock(modified_code)
                            if (func_block not in outputs):
                                outputs.append(func_block)
                                unique = unique + 1
                    else:
                        failed_path = os.path.join(RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "response", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"_response_failed_regression.txt")
                        write_file(failed_path, model_response,
                                   create_dir=True)
                    if cur_sec_test_res['if_passed'] == False:
                        vulnerable = vulnerable + 1
                        failed_path = os.path.join(RESULT_DIR, vul.vul_id, PROJECT_NAME+vul.vul_id, cur_prompt, "response", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"_response_failed_security.txt")
                        os.rename(path_response, failed_path)

                    print("[Timer]: {} End - Prompt #{}, temperature {}, repeat_idx #{}, {}".format(
                        vul.vul_id, prompt_idx, temper, repeat_idx, get_current_time()))

                print("Total: ", total)
                print("Compilable: ", temper, compilable)
                print("plausible: ", temper,  plausible)
                print("unique: ", temper, unique)
                print("Functional: ", temper, functional)
                print("Vulnerable: ", temper, vulnerable)
                print("[Timer]: {} End - Prompt #{}, temperature {}, {}".format(
                    vul.vul_id, prompt_idx, temper, get_current_time()))

            print("Total: ", total)
            print("Compilable: ", compilable)
            print("plausible: ", plausible)
            print("unique: ", unique)
            print("Functional: ", functional)
            print("Vulnerable: ", vulnerable)
            res_content = "Total: " + str(total)+'\n'+"Compilable: " + str(compilable)+'\n'+"plausible: " + str(
                plausible)+'\n' + "unique: " + str(unique)+'\n' + "Functional: " + str(functional)+'\n' + "Vulnerable: " + str(vulnerable)+'\n'

            write_file(res_path, res_content, create_dir=True)

            print("[Timer]: {} End - Prompt #{},{}".format(vul.vul_id,
                  prompt_idx, get_current_time()))
