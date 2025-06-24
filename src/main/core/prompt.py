import os
from main.utils.prompt_generator_util import get_code_context
import os
from main.utils.file_util import read_file, extract_content_within_line_range


def first_prompt(repo_dir, vul, prompt_dir):      
    # prompt = "Following is a vulnerable function in C and each line of it starts with the corresponding line number:\n\n{}\n"\
    #     "The code contains the vulnerability {}. "\
    #     "The vulnerable line number is {} and the corresponding vulnerable code is \"{}\". "\
    #     "Please generate a complete fixed version of the function with minimal change. "\
    #     "Please only respond code. ".format(
    #         vul_code_fun_with_line_num, vul.vul_description, vul_line_num, vul_code_line.strip())
    # prompt = "Q: Following \"C\" code snippet has a {} vulnerability. The vulnerable line numbers are {}. Generate a fix for this.\
    #  Your fix should not break any functionality of the function. Do not add new data type or library. Do not respond with whole code snippet. Output only the modified code with line number  in a \"json object\" with \"LineNo\" and \"EditLine\" as keys.\
    #   \nModified lines: {{\"LineNo\":[], \"EditLine\":[]}}\n{}\nA: Let's think step by step.".format(
    #         vul.vul_description, vul_line_num, vul_code_fun_with_line_num)
    vul_code_fun_with_line_num, vul_line_num, initial_block = get_code_context(repo_dir, vul)
    
    ###########ZERO SHOT CoT
    
    prompt = "Q: Following \"C\" code snippet has a {} vulnerability. The vulnerable line numbers are {}. Generate a fix for this.\
        Your fix should not break any functionality of the function.\n {}\n A: Let's think step by step.".format(
            vul.vul_description, vul_line_num, vul_code_fun_with_line_num)

    return prompt, initial_block


def following_prompt(repo_dir, vul, compile_err_msg, fun_err_msg, sec_err_msg, cur_changed_line_cnt, prompt_dir, cur_change):    
    ###########PROMPT TYPE 1
    # prompt = "Following \"C\" code snippet has a " + vul.vul_description + \
    #     " vulnerability. The vulnerable line numbers are "+ str(vul_line_num) + "\n" + vul_code_fun_with_line_num + "\n"
    
    vul_code_fun_with_line_num, vul_line_num, initial_block = get_code_context(repo_dir, vul)
    #######ZERO SHOT CoT 
    prompt = "Following \"C\" code snippet has a {} vulnerability. The vulnerable line numbers are {}.\n{}\n".format(
                vul.vul_description, vul_line_num, vul_code_fun_with_line_num) 

    prompt += f"The following are the code changes you suggested: {cur_change}\n"

    # compilation error
    if compile_err_msg is not None:
        prompt += ("The code changes are not correct. The patch has the following compilation error:\n" +
                   compile_err_msg + ".\n")

        # if fun_err_msg is not None:
        #     prompt += ("The code changes are not correct. The patch does not pass the regression test. Following is the error message:\n" + fun_err_msg + ".\n")
    if len(fun_err_msg) != 0:
        prompt += "The code change is not correct. The patch does not pass the regression test."
        if len(fun_err_msg) == 1:
            prompt += " The failed test case is "+fun_err_msg[0]+"\n"
        elif len(fun_err_msg) > 1:
            prompt += " The failed test cases are " + \
                ", ".join(fun_err_msg[:-1]) + \
                " and "+fun_err_msg[-1]+"\n"
    if sec_err_msg is not None:
        prompt += ("The code changes are not correct. The patch does not pass the security test. Following is the error message:\n" + sec_err_msg + ".\n")

    if cur_changed_line_cnt is not None and cur_changed_line_cnt > 3:
        prompt += ("Moreover, the code changes are too big. Generate patch with smaller changes.\n")

    #prompt += "Please regenerate a new fix. Again, generate a complete fixed version of the function. Only respond with code and code should be under 'patch:'."
    # prompt += "Please regenerate a new fix. Do not add new data type or library. Do not respond with whole code snippet. Output only the modified code with line number  in a \"json object\" with \"LineNo\" and \"EditLine\" as keys.\
    #       \nModified lines: {{\"LineNo\":[], \"EditLine\":[]}}"

    #######ZERO SHOT CoT
    prompt += "Please regenerate a new fix. Let's think step by step."

    ###########PROMPT TYPE 1
    # prompt += "Generate a complete fixed version of the function. Only respond with code.\n "
    # prompt += "Fixed:\n" + initial_block

    return prompt, initial_block


def prompt_generator(query_idx, repo_dir, vul, compile_err_msg=None, fun_err_msg=[], sec_err_msg=None, cur_changed_line_cnt=None, prompt_dir=None, cur_change=None):
    # first time query
    if query_idx == 1:
        return first_prompt(repo_dir, vul, prompt_dir)
    elif query_idx > 1:
        return following_prompt(repo_dir, vul, compile_err_msg, fun_err_msg, sec_err_msg, cur_changed_line_cnt, prompt_dir, cur_change)
