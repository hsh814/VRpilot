"""
-------------------------------------------------
   File Name:       rq2
   Description:     Compare with VJBench 
   by using GPT-3.5-turbo model
-------------------------------------------------
"""


import os
import json
import sys
import subprocess
import re


GPT_DIR = os.path.abspath(__file__)[: os.path.abspath(__file__).rindex('/') + 1]

sys.path.insert(1, GPT_DIR +'../')

from util import dedent_the_whole_method,vjbench_bug_id_list,vul4j_bug_id_list,cve_int_to_name
from interact_with_GPT import interact_with_openai
from util import extract_correct_method_code, translate_code, cve_name_to_int, info_json, vjbench_json, ROOT_PATH, VJBENCH_DIR, cve_test_java_file, cve_compile_java_file 
from build_vjbench import checkout_vul
from prompt import prompt_generator, trim_prompt
from gpt_util import if_exceed_token_limit, write_file, append_str_to_file, get_current_time, delete_folder
from interact_with_GPT import interact_with_openai
from diff_util import print_diff
from extract_error_using_GPT import err_msg_from_build_log, err_msg_from_test_log




def setup_result_folders(filename):
    RESULT_DIR = os.path.join(GPT_DIR,"result")
    if not os.path.exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    exp_dir = os.path.join(RESULT_DIR, filename)
    # if not os.path.exists(exp_dir):
    #     os.makedirs(exp_dir)
    #prompt_type_dir = os.path.join(exp_dir, prompt_type)
    if os.path.exists(exp_dir):
        delete_folder(exp_dir)
    os.mkdir(exp_dir)
    os.mkdir(os.path.join(exp_dir, "prompt"))
    os.mkdir(os.path.join(exp_dir, "response"))
    os.mkdir(os.path.join(exp_dir, "patch"))
    os.mkdir(os.path.join(exp_dir, "regressionTest"))
    os.mkdir(os.path.join(exp_dir, "buildError"))

    return exp_dir


def extract_err_msg_from_build_log (build_log, err, buggy_method_start, buggy_method_end, filename):
    if "BC-Java" in filename or "Halo-1" in filename:
        err = err[err.find("error:"):]
        err = err[:err.find("Note:")]
        return err
    else:
        line_regex = r'.java:\[([0-9]+),([0-9]+)\] error:'
        line_regex1 = r'.java:\[([0-9]+)\] error:'
        line_regex2 = r'.java:([0-9]+):([0-9]+):'
        line_regex3 = r'.java:([0-9]+): error:'
        if (filename in ['Jinjava-1', 'Retrofit-1']):
            lines = err.split("\n")
        else:
            lines = build_log.split("\n")
        error = ""
        count = 0
        for i in range (0,len(lines)):
            line = lines[i]
            match = re.search(line_regex, line)
            match1 = re.search(line_regex1, line)
            match2 =  re.search(line_regex2, line)
            match3 = re.search(line_regex3, line)
            line_no = ""
            if (match is not None or match1 is not None or match2 is not None or match3 is not None):
                if (match is not None):
                    line_no, char_idx = match.groups()
                elif(match1 is not None):
                    line_no= match1.groups()[0]
                elif (match2 is not None):
                    line_no= match2.groups()[0]
                elif (match3 is not None):
                    line_no= match3.groups()[0]
                    #print(line_no)
                if (int(line_no) >= buggy_method_start - 50 and int(line_no) <= buggy_method_end + 50):
                    #print("here")
                    names = line[:line.find(".java")].split("/")
                    error += names[len(names) - 1]+line[line.find(".java"):]+"\n"
                    if(filename in 'Retrofit-1'):
                        error += lines[i + 1]
                    count += 1
            if(count == 15):
                break

        #print(error)
        return error
        # log = err.split("\n")
        # msg = ""
        # for line in log:
        #     if ("error" in line):
        #         msg += line
        # return msg
    return  ""

def extract_err_msg_from_test_log(test_log, filename):
    if "BC-Java" in filename or "Halo-1" in filename:
        failes = []
        lines = test_log.split("\n")
        for line in lines:
            if ("FAILED" in line or "failed" in line):
                failes.append(line)
        return failes
    elif 'Retrofit-1' in filename:
        lines = test_log.split("\n")
        found = False
        failes =[]
        for i in range (0, len(lines)):
            line = lines[i]
            if "[ERROR] Failures:" in line:
                found = True
            elif "[ERROR]" in line and found:
                failes.append(line)
            elif "[ERROR]" not in line and found:
                found = False
        return failes
    else:    
        test_log = test_log[test_log.find("Failed tests:")+ len("Failed tests:"):]
        test_log = test_log[:test_log.find("Tests run:")]
        return test_log.split("\n")

def restore_changes (restore_cmd, project_path):
    p =  subprocess.Popen(restore_cmd.split(), cwd=project_path,stdout=subprocess.PIPE)
    p.communicate()    

if __name__ == "__main__":

    # parameter setting
    CUR_RQ = "RQ2"
    #PROJECT_NAME = "libtiff"
    MODEL_NAME = "gpt-3.5-turbo"  # ["gpt-4-0314", "gpt-3.5-turbo"]
    TEMPERATURES =[0.6] #[0,0.25,0.5,0.75,1]
    REPEAT = 10
    MAX_QUERY_CNT = 5
    #RESULT_DIR = os.path.join(PRO_DIR, "result", CUR_RQ, )

    bug_range_list =  vjbench_bug_id_list+vul4j_bug_id_list
    trans = ["structure_change_only", "rename_only", "rename+code_structure","original"]

    input_file = os.path.join(GPT_DIR,"inputs","input-{}.json".format( trans[3]))
    #input_file = os.path.join(GPT_DIR,"inputs","input-{}.json".format( trans[2]))
    incoder_output = json.load(open(input_file, 'r'))

    # examples = {'Jenkins-2': "Exposure of Sensitive Information to an Unauthorized Actor",
    #     'Jenkins-1': "Exposure of Sensitive Information to an Unauthorized Actor"   
    #     }
    examples = {"Netty-1": "Inconsistent Interpretation of HTTP Requests",
                "Netty-2": "Inconsistent Interpretation of HTTP Requests",
                "Json-sanitizer-1": "Improper Neutralization of Input During Web Page Generation",
                "Ratpack-1": "Improper Neutralization of Special Elements in Output Used by a Downstream Component",
                "Flow-1": "Encoding Error",
                "Flow-2": "Improper Input Validation",
                "Quartz-1": "Improper Restriction of XML External Entity Reference",
                'Jenkins-2': "Exposure of Sensitive Information to an Unauthorized Actor",
                "BC-Java-1":"Improper Verification of Cryptographic Signature",
                "Halo-1":"Improper Limitation of a Pathname to a Restricted Directory",
                "Jenkins-3":"Exposure of Sensitive Information to an Unauthorized Actor",
                "Jenkins-1": "Exposure of Sensitive Information to an Unauthorized Actor",
                "Jinjava-1": "",
                "Retrofit-1":"Improper Restriction of XML External Entity Reference"
                #"Pulsar-1": "Incorrect Authorization",
                }
    

    #for filename in incoder_output['data']:
    for filename in examples:
        raw_vul_id = "VUL4J-{}".format(cve_name_to_int[filename])
        with open(info_json, "r") as f:
            all_info_list = json.load(f)

        for info in all_info_list:
            if info["vul_id"] == raw_vul_id:
                buggy_file_path = info["buggy_file"]
                tmp = buggy_file_path.split("/")
                buggy_file_name = tmp[len(tmp) - 1]
                buggy_method_start = info["buggy_method_with_comment"][0][0]
                buggy_method_end = info["buggy_method_with_comment"][0][1]
                buggy_line_start = info["buggy_line"][0][0]
                cve_id = info["CVE_id"]
                project_path = os.path.join(VJBENCH_DIR, filename)
                buggy_file_path = os.path.join(project_path,buggy_file_path)
                if (len(info["buggy_line"][0])==1):
                    buggy_line_end = buggy_line_start
                else:
                    buggy_line_end = info["buggy_line"][0][1]
                with open(vjbench_json, "r") as f:
                    vjbench_info = json.load(f)
                compile_cmd = vjbench_info[filename]["compile_cmd"]
                test_cmd = vjbench_info[filename]["test_cmd"]
                restore_cmd = "git checkout HEAD {}".format(vjbench_info[filename]["buggy_file_path"])
                checkout_vul(filename)
                p =  subprocess.Popen(restore_cmd.split(), cwd=project_path,stdout=subprocess.PIPE)
                p.wait()
                break

        # gatekeeper
        if_build_sucess, build_log, err = cve_compile_java_file(project_path, compile_cmd)
        if (not if_build_sucess):
            print("Build failed, something wrong here!", get_current_time())
            exit(0)

        # gatekeeper
        if_test_pass, test_log = cve_test_java_file(project_path, test_cmd)
        if if_test_pass == True:
            print("{} The original version is secure, something wrong here!".format(
                filename), get_current_time())
            exit(0)

        # Saves the unique responses
        init_prompt = "new"
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

        
        #Create result folder and saves response, prompt there
        cur_prompt_type_dir = setup_result_folders(filename)

        res_path = os.path.join(cur_prompt_type_dir, "result.txt")
        if os.path.exists(res_path):
            print("Result {} already exists".format(filename))
            continue
        res_content = ""
        # iterate through the 5 temperatures
        for temper in TEMPERATURES:
            # Initialize the conversation history
            conversation_history = ""
            LOG_PREFIX = "### RQ:{}\n\n### Project:{}\n".format(CUR_RQ, filename)

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
                    restore_changes(restore_cmd=restore_cmd, project_path=project_path)
                    print("[Timer]: {} Start - temperature {}, repeat_idx #{}, query_idx #{},{}".format(
                        filename, temper, repeat_idx, query_idx, get_current_time()))
                    code_input = incoder_output['data'][filename]['input']
                    initial_code = incoder_output['data'][filename]['initial_code']
                    buggy_line = incoder_output['data'][filename]['buggy_line']
                    #cwe = "Exposure of Sensitive Information to an Unauthorized Actor" #"CWE-347" #CHANGE THIS
                    cwe = examples[filename]
                    prompt = prompt_generator(query_idx, GPT_DIR, code_input,cwe, buggy_line, init_prompt, compile_err_msg=cur_compile_err_msg, fun_err_msg=cur_fun_err_msg,cur_changed_line_cnt=cur_changed_line_cnt, cur_change=cur_change)
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
                        filename, get_current_time()))
                
                    model_response = interact_with_openai(MODEL_NAME, prompt, temper)

                    ###########ZERO SHOT CoT
                    prompt += "\n" + model_response + "\n Therefore the fixed code is\n" + initial_code
                    if_exceed, num_of_tokens = if_exceed_token_limit(
                        prompt, MODEL_NAME)
                    actual_prompt = prompt
                    if (if_exceed):
                        print("Number of token: ", num_of_tokens)
                        prompt = trim_prompt(query_idx,prompt,cur_change,cur_changed_line_cnt,cur_compile_err_msg, cur_fun_err_msg)
                        path_actual_prompt = os.path.join(cur_prompt_type_dir, "prompt", "temp_"+str(
                        temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"_actual_prompt.txt")
                        write_file(path_actual_prompt, actual_prompt, create_dir=True)

                    model_response = interact_with_openai(MODEL_NAME, prompt, temper)


                    print("[Timer] {} End to get Response from ChatGPT, {}".format(
                        filename, get_current_time()))

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
                    #exit(0)
                    match_line = incoder_output['data'][filename]['match_line']
                    response = '\n'.join([i.lstrip('0123456789') for i in model_response.split("\n")])
                    #print(match_line, response.find(match_line))
                    if (response.find(match_line) != -1):
                        output = response[response.find(match_line):]
                    else:
                        output = response
                    #print("@@@@@"+output)
                    #print("$$$$"+initial_code)
                    if (output.rfind("}") != -1):
                        output = output[ : output.rfind("}") + 1]
                    elif filename in 'Jinjava-1':
                        output = output[ : output.rfind(".build();") + len(".build();")]
                    if (initial_code not in output):
                        output = initial_code +output
                    print(output) 

                    #continue
                    append_str_to_file("### Query #{} Modified_code:{}\n\n".format(query_idx,
                        output), cur_log_fpath)
                   

                    diff_str, cur_changed_line_cnt = print_diff(
                        [i.lstrip('0123456789 ') for i in code_input.split('\n')],[i.lstrip(' ') for i in output.split('\n')])
                    append_str_to_file(
                        "### Query #{} Diff:\n{}\n\n".format(query_idx, diff_str), cur_log_fpath)

                    #tranformed
                    # if trans != "original" and trans != "structure_change_only":
                    #     output = translate_code(output,filename)
                    #print("Translation ")
                    #print(output)
                    #exit(0)
                    # inject the model's response into project
                    with open(buggy_file_path, "r") as f:
                        lines = f.readlines()
                    with open(buggy_file_path, "w") as f:
                        f.writelines(lines[:buggy_method_start-1])
                        f.write(output)
                        f.writelines(lines[buggy_method_end:])

                    patch_path = os.path.join(cur_prompt_type_dir, "patch", "temp_"+str(
                        temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+ buggy_file_name)
                    write_file(patch_path, open(buggy_file_path, "r").read(), create_dir=True)

                    # path_build_log = os.path.join(cur_prompt_type_dir, "buildError", "temp_"+str(
                    #         temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"buildLog.txt")
                    # " > "+path_build_log+" 2>&1"
                    if_build_sucess, build_log, err = cve_compile_java_file(project_path, compile_cmd)
                    #print(cve_compile_java_file(project_path, compile_cmd))
                    #exit(0)
                    if if_build_sucess == False:  # if patch is NOT compilable
                        print("build faild")
                        #cur_compile_err_msg = extract_err_msg_from_build_log(build_log, err, buggy_method_start, buggy_method_end, filename)
                        cur_compile_err_msg = err_msg_from_build_log(build_log, err, buggy_method_start, buggy_method_end, filename, MODEL_NAME)
                        if (str(ROOT_PATH) in cur_compile_err_msg):
                            cur_compile_err_msg = cur_compile_err_msg.replace(str(ROOT_PATH),"")
                        #print(cur_compile_err_msg)
                        
                        path_build_log = os.path.join(cur_prompt_type_dir, "buildError", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"buildLog.txt")
                        write_file(path_build_log, build_log+"\n"+err, create_dir=True)
                        #print("rq2.py "+cur_compile_err_msg)

                        reject_path = os.path.join(cur_prompt_type_dir, "response", "temp_"+str(
                            temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"_response_reject.txt")
                        os.rename(path_response, reject_path)
                        append_str_to_file("### Query #{} ends because of model response is not compilable. Build log:\n{}\n\n".format(
                            query_idx, cur_compile_err_msg), cur_log_fpath)
                        cur_fun_err_msg = []
                        cur_sec_err_msg = None
                        #exit(0)    

                    else:
                        cur_compile_err_msg = None
                        if (query_idx == 1):
                            without_feedback_compilable += 1
                        cur_compilable = cur_compilable + 1
                        if_test_pass, test_log = cve_test_java_file(project_path, test_cmd)

                        path_regression_log = os.path.join(
                            cur_prompt_type_dir, "regressionTest", "temp_"+str(temper)+"_itr_"+str(repeat_idx)+"_query_"+str(query_idx)+"regressionLog.txt")
                        write_file(path_regression_log,
                                   test_log, create_dir=True)


                        if (if_test_pass):
                            res_content = res_content + \
                                f"Correct response found for {filename} at temperature {temper}, iteration {repeat_idx}, query idx {query_idx}\n"
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

                        if (not if_test_pass):
                            failed_path = os.path.join(cur_prompt_type_dir, "response", "temp_"+str(temper)+"_itr_"+str(
                                repeat_idx)+"_query_"+str(query_idx)+"_response_failed_regression.txt")
                            write_file(failed_path, model_response,
                                       create_dir=True)
                            
                            cur_fun_err_msg = err_msg_from_test_log(test_log, filename, MODEL_NAME)
                            if (str(ROOT_PATH) in cur_fun_err_msg):
                                cur_fun_err_msg = cur_fun_err_msg.replace(str(ROOT_PATH),"")

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
        
        #break


