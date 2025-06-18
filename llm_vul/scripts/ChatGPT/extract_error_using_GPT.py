from gpt_util import if_exceed_token_limit
from interact_with_GPT import interact_with_openai

def err_msg_from_build_log (build_log, err, buggy_method_start, buggy_method_end, filename, model_name):
    log_line = (build_log + err).split("\n")
    print("Total line number: ", len(log_line))
    if (len(log_line) > 50 ):
        log_line = log_line[len(log_line) - 50:]
    log = "\n".join(log_line)
    prompt = "Extract compilation error message from the following log.\n"+log
    if_exceed, num_of_tokens = if_exceed_token_limit(prompt, model_name)
    print("Total number of token ",num_of_tokens)
    if if_exceed:
        #print(num_of_tokens)
        log_line = log_line[len(log_line)-25:]
        log = "\n".join(log_line)
        prompt = "Extract compilation error message from the following log.\n"+log
    model_response = interact_with_openai(model_name, prompt, 0.0)
    return model_response

def err_msg_from_test_log(test_log, filename, model_name):
    log_line = test_log.split("\n")
    total_line = len(log_line)
    print("Total line number: ", total_line)
    if (len(log_line) > 50 ):
        log_line = log_line[len(log_line) - 50:]

    log = ""    
    for line in log_line:
        if ("Failed to execute goal" in line):
            continue
        log += line + "\n"

    #log = "\n".join(log_line)
    #prompt = "Extract regression test error message from the following log.\n"+log
    prompt = "Extract the failing test cases from the following log.\n"+log+"\nFailing test" 
    if_exceed, num_of_tokens = if_exceed_token_limit(prompt, model_name)
    print("Total number of token ",num_of_tokens)
    if if_exceed:
        #print(num_of_tokens)
        print("Exceed######")
        #limit = int((total_line * 2200)/num_of_tokens)
        log_line = log_line[len(log_line)-25:]
        log = "\n".join(log_line)
        prompt = "Extract the failed test cases from the following log.\n"+log+"\nFailing test" 
    #print(prompt)
    model_response = interact_with_openai(model_name, prompt, 0.0)
    return [model_response]


