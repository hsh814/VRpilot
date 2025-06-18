import os


def first_prompt (template_path,code_input,cwe, buggy_line, prompt_type):
    if prompt_type == 'new':
        prompt = open(os.path.join(template_path,'cot.template'), "r").read()
        lines = ','.join([str(i) for i in buggy_line])
        prompt = prompt.replace("$LINE", lines).replace("$VUL_CODE", code_input).replace("$VUL_NAME", cwe)
    return prompt


def following_prompt(code_input,cwe, buggy_line, prompt_type, compile_err_msg, fun_err_msg, cur_changed_line_cnt, cur_change):
    
    #######ZERO SHOT CoT 
    prompt = "Following \'Java\' code snippet has {} vulnerability. The vulnerable line numbers are {}.\n{}\n".format(
                cwe, buggy_line, code_input) 

    prompt += f"The following are the code changes you suggested: {cur_change}\n"

    # compilation error
    if compile_err_msg is not None:
        #print("prompt.py "+compile_err_msg)
        prompt += ("The code changes are not correct. The patch has the following compilation error:\n" +
                   compile_err_msg + ".\n")

        # if fun_err_msg is not None:
        #     prompt += ("The code changes are not correct. The patch does not pass the regression test. Following is the error message:\n" + fun_err_msg + ".\n")
    if len(fun_err_msg) != 0:
        prompt += "The code change is not correct. The patch does not pass the unit test."
        if len(fun_err_msg) == 1:
            prompt += " The failed test case is "+fun_err_msg[0]+"\n"
        elif len(fun_err_msg) > 1:
            prompt += " The failed test cases are " + \
                ", ".join(fun_err_msg[:-1]) + \
                " and "+fun_err_msg[-1]+"\n"
    
    if cur_changed_line_cnt is not None and cur_changed_line_cnt > 10:
        prompt += ("Moreover, the code changes are too big. Generate patch with smaller changes.\n")


    #######ZERO SHOT CoT
    prompt += "Please regenerate a new fix. Let's think step by step."

    return prompt


def prompt_generator(query_idx, template_path,code_input,cwe, buggy_line, prompt_type, compile_err_msg=None, fun_err_msg=[],cur_changed_line_cnt=None , cur_change=None): 
    # first time query
    if query_idx == 1:
        return first_prompt(template_path,code_input, cwe,buggy_line, prompt_type)
    elif query_idx > 1:
        return following_prompt(code_input, cwe,buggy_line, prompt_type, compile_err_msg, fun_err_msg, cur_changed_line_cnt, cur_change)

def trim_prompt(query_idx,prompt,cur_change,cur_changed_line_cnt,cur_compile_err_msg, cur_fun_err_msg):
    if (query_idx > 1):
        idx1 = prompt.find("The following are the code changes you suggested")
        idx2 = prompt.find("Please regenerate a new fix")
        new_prompt = prompt[:idx1]+"\n"+prompt[idx2:]
        #print(new_prompt) 
        return new_prompt