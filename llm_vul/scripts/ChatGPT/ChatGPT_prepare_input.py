import subprocess
import os
import json
from pathlib import Path
import sys
INCODER_DIR = os.path.abspath(__file__)[: os.path.abspath(__file__).rindex('/') + 1]

sys.path.insert(1, INCODER_DIR+'../') # utils file

from util import dedent_the_whole_method,vjbench_bug_id_list,vul4j_bug_id_list,cve_int_to_name
#from vutil import cve_int_to_name

bug_range_list =  vjbench_bug_id_list+vul4j_bug_id_list


def genearte_incoder_input(output_file, trans):
    codex_input = {'config': comment_config, 'data': {}}
    #print("Total bug:", len(bug_range_list))
    for vul_int in bug_range_list:
        vul_id = "VUL4J-{}".format(vul_int)
        if vul_int > 1000:
            vul_id = cve_int_to_name[vul_int]
        VUL_FOLDER = os.path.join(INCODER_DIR+'../../VJBench-trans', vul_id)
        bug_location_file = os.path.join(VUL_FOLDER, "buggyline_location.json")
        # read the bug location file
        with open(bug_location_file, 'r') as f:
            buggy_line_dict = json.load(f) 
        buggy_line_list = buggy_line_dict[  trans]
        if trans == "structure_change_only":
            buggy_file = os.path.join(VUL_FOLDER, "{}_code_structure_change_only.java".format(vul_id))
        elif trans == "rename+code_structure":
            buggy_file = os.path.join(VUL_FOLDER, "{}_full_transformation.java".format(vul_id))
        elif  trans== "rename_only":
            buggy_file = os.path.join(VUL_FOLDER, "{}_rename_only.java".format(vul_id))
        elif trans== "original":         
            buggy_file = os.path.join(VUL_FOLDER, "{}_original_method.java".format(vul_id))
        if not os.path.exists(buggy_file):
            continue
    
        buggy_line_start = buggy_line_list[0][0]
        if (len(buggy_line_list[0])==1):
            buggy_line_end = buggy_line_start
        else:
            buggy_line_end = buggy_line_list[0][1]
    
        #####################################################
        buggy_file_abs_path = buggy_file
        with open(buggy_file_abs_path) as f:
            lines = f.readlines()
        # copy the lines to a new file from the buggy method start to the buggy method end
        buggy_lines = []

        buggy_method_start = 1
        buggy_method_end = len(lines)

    
        for i in range(buggy_line_start, buggy_line_end + 1):
            buggy_lines.append(i)


        vul_code_fun_with_line_num = ""
        #vul_code_line = ""
        vul_line_num = ""
        #start = vul.vul_code_block_start_line

        for line_num in range(0, buggy_method_end):
            vul_code_fun_with_line_num += str(line_num+1) + \
                " " + lines[line_num]

        filename = vul_id
        codex_input['data'][filename] = {
    
            'input':vul_code_fun_with_line_num,
            'buggy_line': buggy_lines,
            'initial_code': ''.join([i for i in lines[:2]]),
            'match_line': lines[2].strip()
        }
        # dump to json file
        with open(output_file, 'w') as f:
            json.dump(codex_input, f, indent=2)



with_comment = True


if __name__ == "__main__":

    for trans in [
        # "structure_change_only", 
        # "rename_only", 
        #"rename+code_structure"
        "original"
        ]:
  
        if not with_comment:
            comment_config = "NO_COMMENT"
        else:
            comment_config = "WITH_COMMENT"
        input_file = os.path.join(INCODER_DIR,"inputs","input-{}.json".format( trans))
        genearte_incoder_input(input_file, trans)