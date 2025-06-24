import os
import re
from main.utils.file_util import read_file, extract_content_within_line_range
from main.data_structure.vulnerability import Project, Vulnerability

def get_vulnerable_function_lines(language, vulnerable_file_contents, start_line_index):
    if language == 'python':
        comment_char = '#'
        detect_function_regex = '^\s*def (.*?)\('
    elif language == 'c':
        comment_char = '//'
        detect_function_regex = """^[a-zA-Z_][a-zA-Z_0-9*\(\)\[\]]*\s*[a-zA-Z_0-9*\(\)\[\]]*\s*[a-zA-Z_0-9*\(\)\[\]]*\s*[a-zA-Z_0-9*\(\)\[\]]+\s+[a-zA-Z_0-9]+\s*\([a-zA-Z0-9*_\s\[\],]*\)(?:\s*{|\s\/\*[\sA-Za-z0-9_.,*#\[\]\\\/;'\"-]+\*\/\s*{)"""
    else:
        raise Exception('unsupported language ' + language)

    #################THIS METHOD WORKS FOR FUNCTION LEVEL#####################

    #
    vulnerable_file_contents_str = ''.join(vulnerable_file_contents)
    vulnerable_file_contents_str = vulnerable_file_contents_str.replace('\r', '')
    #find the end of the function openers using the detect_function_regex
    function_def_boundaries = []
    for match in re.finditer(detect_function_regex, vulnerable_file_contents_str, re.MULTILINE):
        function_def_boundaries.append([match.start(), match.end()])

    #print(function_def_boundaries)

    #we have the end of the function, crop the lines at that point
    ##TODO: COME BACK TO THIS

    #for each function index, determine what line it finishes on by counting the number of newlines before it
    function_def_num_newlines = []
    for function_def_boundary in function_def_boundaries:
        function_def_num_newlines.append(
            [
                vulnerable_file_contents_str.count('\n', 0, function_def_boundary[0]), 
                vulnerable_file_contents_str.count('\n', 0, function_def_boundary[1])
            ]
        )   
    #print(function_def_num_newlines)
    #print(start_line_index)
    closest_newline_index = 0
    closest_newline_value = 0
    for i in range(len(function_def_num_newlines)):
        if function_def_num_newlines[i][1] > start_line_index:
            break
        if function_def_num_newlines[i][1] > closest_newline_value:
            closest_newline_value = function_def_num_newlines[i][1]
            closest_newline_index = i

    vulnerable_function_start_line_num = function_def_num_newlines[closest_newline_index][0]
    vulnerable_function_end_line_num = function_def_num_newlines[closest_newline_index][1]

    #print("function starts on line " + str(vulnerable_function_start_line_num))
    #print("function ends on line " + str(vulnerable_function_end_line_num))

    
    ##OLD METHOD

    #get the number of whitespace chars in the first line of the function index
    vulnerable_function_line = vulnerable_file_contents[vulnerable_function_start_line_num]
    vulnerable_function_line_stripped = vulnerable_function_line.lstrip()
    vulnerable_function_whitespace_count = len(vulnerable_function_line) - len(vulnerable_function_line_stripped)

    #print("Vulnerable function no. of whitespace chars:", vulnerable_function_whitespace_count)

    #if language == 'python':
    #starting at the end function line number, go forwards until you find a non-comment line that has the same indentation level
    vulnerable_function_end_index = 0
    for i in range(vulnerable_function_end_line_num+1, len(vulnerable_file_contents)):
        line = vulnerable_file_contents[i]
        line_stripped = line.lstrip()
        if len(line_stripped.rstrip()) == 0:
            continue
        if line_stripped[0:len(comment_char)] == comment_char:
            continue

        if len(line) - len(line_stripped) == vulnerable_function_whitespace_count:
            break
        vulnerable_function_end_index = i + 1
        
    #print("Vulnerable function end index:", vulnerable_function_end_index)
    #print("Vulnerable function end line:", vulnerable_file_contents[vulnerable_function_end_index])

    if language == 'c' and vulnerable_file_contents[vulnerable_function_end_index].strip() == '}':
        vulnerable_function_end_index += 1 #we'll include the closing brace in the vulnerable function for C

    #make the prompt lines from 0 to vulnerable_function_index+1 (line after the function)
    vulnerable_file_prepend_lines = vulnerable_file_contents[0:vulnerable_function_start_line_num]

    #IMPORTANT: we assume that the vulnerable function has a newline between function start "{" or ":" and the body
    vulnerable_file_function_def_lines = vulnerable_file_contents[vulnerable_function_start_line_num:vulnerable_function_end_line_num+1]

    #make the vulnerable lines from prompt_line_end_index to start_line_index
    vulnerable_file_function_pre_start_lines = vulnerable_file_contents[vulnerable_function_end_line_num+1:start_line_index]

    #start line onwards
    vulnerable_file_function_start_lines_to_end = vulnerable_file_contents[start_line_index:vulnerable_function_end_index]

    #make the append lines from start_line_index to the end
    vulnerable_file_append_lines = vulnerable_file_contents[vulnerable_function_end_index:]

    #print("The function began on line", vulnerable_function_index)
    return (vulnerable_file_prepend_lines, vulnerable_file_function_def_lines, vulnerable_file_function_pre_start_lines, vulnerable_file_function_start_lines_to_end, vulnerable_file_append_lines)
 

def get_code_context(repo_dir, vul: Vulnerability):
    vulnerable_file_path = os.path.join(repo_dir, vul.vul_code_file_rel_path)
    vul_code_fun = extract_content_within_line_range(vulnerable_file_path, vul.vul_code_block_start_line, vul.vul_code_block_end_line)
    initial_block = ""
    # if (vul.vul_id == "cve_2016_10094"): 
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 2761, 2779)
    #     vul_code_fun += "\n" + extract_content_within_line_range (vulnerable_file_path, 2883, 2930)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 2883, 2885)

    # elif (vul.vul_id == "cve_2017_7601"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 1576, 1657)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 1625, 1627)

    # elif (vul.vul_id == "cve_2016_3623"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 70, 101)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 96, 97)
    #     # vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 48, 51)
    #     # vul_code_fun += "\n" +  extract_content_within_line_range (vulnerable_file_path, 249, 278)
    #     # initial_block = extract_content_within_line_range (vulnerable_file_path, 249, 251)

    # elif (vul.vul_id == "cve_2017_7595"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 1576, 1593)
    #     vul_code_fun += "\n" + extract_content_within_line_range (vulnerable_file_path, 1686, 1707)
    #     vul_code_fun += "\n" + "return (1);"
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 1576, 1579)
    
    # elif (vul.vul_id == "cve_2016_5321"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 951, 1096)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 951, 957)

    # elif (vul.vul_id == "cve_2014_8128"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 551, 576)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 551, 554)

    # elif (vul.vul_id == "EF02_02"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 35, 42)
    #     vul_code_fun += "\n" + extract_content_within_line_range (vulnerable_file_path, 48, 142)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 102, 104)

    # elif (vul.vul_id == "cve_2018_19664"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 482, 555)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 482, 486)
    #     # vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 96, 171)
    #     # initial_block = extract_content_within_line_range (vulnerable_file_path, 96, 101)

    # elif (vul.vul_id == "cve_2012_2806"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 301, 371)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 301, 305)

    # elif (vul.vul_id == "cve_2017_5969"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 1158, 1222)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 1158, 1160)

    # elif (vul.vul_id == "cve_2012_5134"):
    #     # vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 3893, 4116)
    #     # initial_block = extract_content_within_line_range (vulnerable_file_path, 4075, 4075)
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 3893, 3922)
    #     vul_code_fun += "\n" +  extract_content_within_line_range (vulnerable_file_path, 4078, 4081)
    #     vul_code_fun += "\n" +  extract_content_within_line_range (vulnerable_file_path, 4099, 4116)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 3893, 3895)
    
    # elif (vul.vul_id == "cve_2016_1838"):
    #     vul_code_fun = extract_content_within_line_range (vulnerable_file_path, 9824, 9891)
    #     initial_block = extract_content_within_line_range (vulnerable_file_path, 9824, 9827)

    vul_code_fun_with_line_num = ""
    vul_code_line = ""
    vul_line_num = ""
    start = vul.vul_code_block_start_line
    
    vul_line_num = f"{vul.vul_code_line - vul.vul_code_block_start_line + 1}"

    for line_num in range(0, len(vul_code_fun.split('\n'))):
        vul_code_fun_with_line_num += str(line_num+1) + \
            " " + vul_code_fun.split('\n')[line_num] + "\n"
        # if vul.vul_code_line in vul_code_fun.split('\n')[line_num]:
        #     vul_code_line = vul_code_fun.split('\n')[line_num]
        #     vul_line_num += str(line_num+1) + ","

    # if (vul.vul_id == "cve_2016_3623"):
    #     vul_line_num = "27,28,30,31"
    # elif (vul.vul_id == "cve_2017_7595"):
    #     vul_line_num = "21" 
    # elif (vul.vul_id == "cve_2016_5321"):
    #     vul_line_num = "42; \"for (s = 0; s < spp; s++)\"."
    # elif (vul.vul_id == "EF02_02"):
    #     vul_line_num = "86" 
    # elif (vul.vul_id == "cve_2016_1838"):
    #     vul_line_num = "14"
    # elif (vul.vul_id == "cve_2012_5134"):
    #     vul_line_num = "33"
    # elif (vul.vul_id == "cve_2017_5969"):
    #     vul_line_num = "18, 24, 32, 38"
    # elif (vul.vul_id == "cve_2018_19664"):
    #     vul_line_num = "24,25" 
    # elif (vul.vul_id == "cve_2012_2806"):
    #     vul_line_num = "27" 
    
    return vul_code_fun_with_line_num, vul_line_num, initial_block