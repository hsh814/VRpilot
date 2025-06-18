import re
from main.utils.file_util import read_file, write_file, extract_content_within_line_range
from path_config import CONFIG_DIR
import os
import json
from main.core.interact_with_GPT import interact_with_openai
from main.utils.cmd_util import execute_cmd_with_output
from main.utils.diff_util import print_diff

def extract_code_block_from_markdown_text(md_text):
    return re.findall(r'([\w\W]*?)|^ (.+)$',
                      md_text, re.MULTILINE)


def extract_code(generated_text):
    if (generated_text.lower().find("sorry") != -1):
        return ""
    if (generated_text.lower().find("patch:") != -1):
        code_block = (generated_text[generated_text.lower().index("patch:") + len("patch:"):])
        return code_block
    return ""
    # lower_text = generated_text.lower()
    # if (lower_text.find("patch:") != -1):
    #     code_block = (
    #         generated_text[lower_text.index("patch:") + len("patch:"):])
    #     return code_block

    # if (lower_text.find("patch:") != -1):
    #     code_block = (
    #         generated_text[lower_text.index("patch:") + len("patch:"):])
    #     return code_block
    #generated_lines = generated_text.split("\n")
    # for i in range (0, len(generated_lines)):
    #     if("patch" in generated_lines[i].lower()):
    #         generated_lines = generated_lines[i+1:]
    #         break
            
    # i = 0
    # while("#" in generated_lines[i]):
    #     i = i + 1
    # code = "\n".join(generated_lines[i:])
    # return code

def generate_patch_with_GPT_response (config_file_path, project, generated_text, idx):
    #Read the configuration file to get the start and end line of vulnerable code
    generated_text = extract_code(generated_text)
    if(generated_text == ""):
        return "", ""
    f = open(config_file_path)
    data = json.load(f)
    vul_code_file_rel_path = data["configurations"][idx]['vul_code_file_rel_path']
    cut_line_start = data["configurations"][idx]['vul_code_block_start_line']
    vul_code_block_lines = data["configurations"][idx]['asan_scenario_buginfo']['real_patchinfo'][0]['edit_lines']
    f.close()
    #cut_line_start = 1158
    #cut_line_start = min(vul_code_block_lines)
    cut_line_end = max(vul_code_block_lines)

    contents = read_file (os.path.join(project.working_repo_dir, vul_code_file_rel_path))
    #print(contents)
    program_lines = contents.split("\n")
    prepend_program = "\n".join(program_lines[:cut_line_start-1])
    append_program = "\n".join(program_lines[cut_line_end:])
    
    matched = False
    for i in range(0, 20):
        if len(append_program) > 30-i:
            cutoff_gen = append_program[:30-i].strip()
        else:
            cutoff_gen = append_program.strip()

        #print("cutoff_gen is ", cutoff_gen)

        if len(cutoff_gen) > 0:
            #find where cutoff_gen is in the generated text
            cutoff_gen_index = generated_text.rfind(cutoff_gen)
            if cutoff_gen_index == -1:
                continue
            else:
                #cut the generated text at the cutoff_gen
                matched = True
                generated_text = generated_text[:cutoff_gen_index]
                break

    if not matched:
        print("Not Found $$$$$$$$$$$$$")
        #take everything up to the last newline character (don't take a partial line)
        generated_text = generated_text.rsplit('\n', 1)[0]

        #problem, couldn't find the cutoff_gen in the generated text
        #raise Exception("Couldn't find the cutoff_gen in the generated text")
    #print(generated_text)
    new_contents = prepend_program + "\n" + generated_text + append_program
    
    return new_contents, generated_text    


def generate_patch_with_GPT_response1(config_file_path, project, generated_text, idx):

    # Read the configuration file to get the start and end line of vulnerable code
    
    f = open(config_file_path)
    data = json.load(f)
    vul_code_file_rel_path = data["configurations"][idx]['vul_code_file_rel_path']
    cut_line_start = data["configurations"][idx]['vul_code_block_start_line']
    vul_code_block_lines = data["configurations"][idx]['asan_scenario_buginfo']['real_patchinfo'][0]['edit_lines']
    vul_id = data["configurations"][idx]["vul_id"]
    f.close()
    # cut_line_start = 1158
    
    cut_line_end = max(vul_code_block_lines)
    #contents = read_file (project)
    ################Need to change this later##################
    contents = read_file(os.path.join(
        project.working_repo_dir, vul_code_file_rel_path))
    # print(contents)
    program_lines = contents.split("\n")
    ######for EF01
    if vul_id == "EF01":
        cut_line_start = min(vul_code_block_lines)
        begining_window = data["configurations"][idx]["begining_window"]
        end_window = data["configurations"][idx]["end_window"]
        prepend_program = "\n".join(program_lines[:cut_line_start-1-1])
        append_program = "\n".join(program_lines[end_window:])
        if (generated_text.lower().find("sorry") != -1):
            return "", ""
        begin_cut = generated_text.find(begining_window)
        #print(begining_window)
        #print(begin_cut)
        if (begin_cut >= 0):
            generated_text = generated_text[begin_cut + len(begining_window):]
    elif vul_id == "EF02_01":
        cut_line_start = min(vul_code_block_lines)
        begining_window = data["configurations"][idx]["begining_window"]
        prepend_program = "\n".join(program_lines[:cut_line_start-1])
        append_program = "\n".join(program_lines[cut_line_end + 1:])
        if (generated_text.lower().find("sorry") != -1):
            return "", ""
        begin_cut = generated_text.find(begining_window)
        if (begin_cut >= 0):
            generated_text = generated_text[begin_cut + len(begining_window):]
        
    elif vul_id == "EF02_02":
        begining_window = data["configurations"][idx]["begining_window"]
        prepend_program = "\n".join(program_lines[:cut_line_start-1])
        append_program = "\n".join(program_lines[cut_line_end:])
        if (generated_text.lower().find("sorry") != -1):
            return "", ""
        begin_cut = generated_text.find(begining_window)
        if (begin_cut >= 0):
            generated_text = generated_text[begin_cut + len(begining_window):]
        else:
            generated_text = ""
    elif vul_id == "EF07":
        cut_line_start = min(vul_code_block_lines)
        print("$$$$$$$$$$$$", program_lines[cut_line_start-2])
        print("@@@@@@@@@@@", program_lines[cut_line_end])
        prepend_program = "\n".join(program_lines[:cut_line_start-1])
        append_program = "\n".join(program_lines[cut_line_end:])
        begining_window = data["configurations"][idx]["begining_window"]
        end_window = data["configurations"][idx]["end_window"]
        if (generated_text.lower().find("sorry") != -1):
            return "", ""
        begin_cut = generated_text.find(begining_window)
        if (begin_cut >= 0):
            generated_text = generated_text[begin_cut + len(begining_window):]
        # end_cut = generated_text.find(end_window)
        # if (end_cut >= 0):
        #     generated_text = generated_text[:end_cut]
        generated_lines = generated_text.split("\n")
        for i in range (0, len(generated_lines)):
            if end_window in generated_lines[i] and "*" not in generated_lines[i]:
                break
        generated_text = "\n".join(generated_lines[:i])
    elif vul_id == "EF08":
        cut_line_start = min(vul_code_block_lines)
        prepend_program = "\n".join(program_lines[:cut_line_start])
        append_program = "\n".join(program_lines[cut_line_end:])
        begining_window = "\n".join(program_lines[cut_line_start - 5:cut_line_start])
        if (generated_text.lower().find("sorry") != -1):
            return "", ""
        begin_cut = generated_text.find(begining_window)
        if (begin_cut >= 0):
            generated_text = generated_text[begin_cut + len(begining_window):]
        else :
            cut = generated_text.find("case PHOTOMETRIC_YCBCR:")
            generated_text = generated_text[cut + len("case PHOTOMETRIC_YCBCR:"):]
            prepend_program = "\n".join(program_lines[:1626])
        end_cut =generated_text.find("break;")
        if (end_cut >= 0):
            generated_text = generated_text[:end_cut]

    else:
        generated_text = extract_code(generated_text)
        if (generated_text == ""):
            return "", ""
        prepend_program = "\n".join(program_lines[:cut_line_start-1])
        append_program = "\n".join(program_lines[cut_line_end:])

        print("###############", program_lines[cut_line_start-2])
        print("###############", program_lines[cut_line_end])
    
    

    # generated_lines = generated_text.split("\n")
    # l = 0
    # while True:
    #     if (("for" in generated_lines[l]) and ("*" not in generated_lines[l])):
    #         break
    #     l += 1
    # generated_text = "\n".join(generated_lines[:l+1])

    #print(generated_text)
    
     




    

    # if generate_mean_logprob_comments and mean_logprob is not None:
    #     prepend_program += "\n" + comment_key + "LM generated repair code follows. mean_logprob: " + mean_logprob + "\n"

    # if include_first_token:
    #     word = program_lines[cut_line_start-1].strip().split(' ')[0]
    #     prepend_program += "\n" + word
    # if not addition_only:
    #     append_program = "\n".join(program_lines[cut_line_end+1:])
    # else:
    #     append_program = "\n".join(program_lines[cut_line_end:])

    # get the first few words of the append program
    # if (generated_text.find("default:") != -1):
    #     generated_text = generated_text[:generated_text.index("default:")]
    # else :

    
    matched = False
    for i in range(0, 20):
        if len(append_program) > 30-i:
            cutoff_gen = append_program[:30-i].strip()
        else:
            cutoff_gen = append_program.strip()

        #print("cutoff_gen is ", cutoff_gen, i)

        if len(cutoff_gen) > 0:
            # find where cutoff_gen is in the generated text
            cutoff_gen_index = generated_text.rfind(cutoff_gen)
            if cutoff_gen_index == -1:
                continue
            else:
                # cut the generated text at the cutoff_gen
                matched = True
                generated_text = generated_text[:cutoff_gen_index]
                break

    if not matched:
        print("Not Found $$$$$$$$$$$$$")
        # take everything up to the last newline character (don't take a partial line)
        generated_text = generated_text.rsplit('\n', 1)[0]

        # problem, couldn't find the cutoff_gen in the generated text
        # raise Exception("Couldn't find the cutoff_gen in the generated text")
    print(generated_text)
    
    
    patch = prepend_program + "\n" + generated_text + append_program
    

    return patch, generated_text


def getFuncBlock(content):
    program_lines = content.split("\n")
    func = []
    for line in program_lines:
        # print(len(line))
        if (line != ""):
            if (line.find("//") == -1):
                func.append(line)
    func = "\n".join(func)
    # print(func)
    return func
    # if(content.find("static void\nxmlDumpElementContent") != -1):
    #     content = content[content.index("static void\nxmlDumpElementContent"): ]
    #     program_lines = content.split("\n")
    #     func = []
    #     for line in program_lines:
    #         # print(len(line))
    #         if(line == ""):
    #             func.append(line)
    #         elif(line.find("//") == -1):
    #             if(line[0] != "}"):
    #                 func.append(line)
    #             else:
    #                 func.append("}")
    #                 break
    #     func = "\n".join(func)
    #     # print(func)
    #     return func
    # else:
    #     return ""

def generate_patch_with_GPT_response_new(config_file_path, project, generated_text, idx):
    # jsonRegex = re.compile(r'\{(?:[^{}]|())*\}')
    # code = (jsonRegex.search(generated_text)).group()
    f = open(config_file_path)
    data = json.load(f)
    vul_code_file_rel_path = data["configurations"][idx]['vul_code_file_rel_path']
    vul_code_block_start_line = data["configurations"][idx]['vul_code_block_start_line']
    f.close()
    
    contents = read_file(os.path.join(
        project.working_repo_dir, vul_code_file_rel_path))
    try :
        prompt = "[no prose]\n[output only JSON]\nFollowing text contains a json object. Please output that json object. \nText: {}\nAnswer: {{\"LineNo\":".format(generated_text)
        print(prompt)
        code = interact_with_openai("gpt-3.5-turbo",prompt,0)
        print("#########################")
        print(code)
        if(code.find("{\"LineNo\":") == -1):
            code = "{\"LineNo\":" + code
            print("modified", code)
        json_data = json.loads(code)
        print("#########################")
        print(json_data)

        # if (json_data == ""):
        #     return "", ""
        line_no = json_data["LineNo"]
        edit_line = json_data["EditLine"]
        print(line_no)
        print(edit_line)        
        # print(contents)
        program_lines = contents.split("\n")
        
        for i in range (0, len(line_no)):
            #old_line =  program_lines[int(line_no[i])+vul_code_block_start_line -2]
            new_line = edit_line[i]
            # if((old_line[len(old_line)-1] != "{") and (new_line[len(new_line)-1] == "{")):
            #     new_line = new_line[:len(new_line)-1]
            #     print("@@@@@@@@@@@", "Modified line ", new_line)
            if (int(line_no[i]) > vul_code_block_start_line):
                program_lines[int(line_no[i])-1] = new_line
            else:
                program_lines[int(line_no[i])+vul_code_block_start_line -2] = new_line

        patch = "\n".join(program_lines[:])
        
        return patch, code
    except Exception as e:
        print("Error while generating new patch", e)
        return contents , code + " #####Error while generating new patch " + str(e)




def make_patch_with_diff (config_file_path, project, generated_text, idx):
    f = open(config_file_path)
    data = json.load(f)
    vul_code_file_rel_path = data["configurations"][idx]['vul_code_file_rel_path']
    cut_line_start = data["configurations"][idx]['vul_code_block_start_line']
    vul_code_block_lines = data["configurations"][idx]['asan_scenario_buginfo']['real_patchinfo'][0]['edit_lines']
    vul_id = data["configurations"][idx]["vul_id"]
    f.close()
    ori_file_path = os.path.join(project.working_project_dir,"temp_code_block.txt")
    responsepath = os.path.join(project.working_project_dir,"response_code_block.txt")
    vulnerable_file_path = os.path.join(project.working_repo_dir, vul_code_file_rel_path)
    content = read_file(vulnerable_file_path)
    program_lines = content.split("\n")
    if (vul_id == "EF07"):
        prepend = "\n".join(program_lines[:2885])
        append = "\n".join(program_lines[2930:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 2885, 2930)
        cut_idx = generated_text.find("unsigned char table_end[2];")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("unsigned char table_end[2];"):]
        cut_idx = generated_text.rfind("#endif")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("#endif")]
    elif (vul_id == "EF08"):
        prepend = "\n".join(program_lines[:1628])
        append = "\n".join(program_lines[1657:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 1625, 1657)
        cut_idx = generated_text.find("sp->v_sampling = td->td_ycbcrsubsampling[1];")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("sp->v_sampling = td->td_ycbcrsubsampling[1];"):]
        cut_idx = generated_text.rfind("break;")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("break;")]
    elif (vul_id == "EF09"):
        # prepend = "\n".join(program_lines[:96])
        # append = "\n".join(program_lines[101:])
        # code_block = extract_content_within_line_range (vulnerable_file_path, 96, 101)
        # cut_idx = generated_text.find("case 'h':")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[cut_idx + len("case 'h':"):]
        # cut_idx = generated_text.rfind("break;")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[:cut_idx + len("break;")]
        prepend = "\n".join(program_lines[:252])
        append = "\n".join(program_lines[278:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 249, 278)
        cut_idx = generated_text.find("uint32 y;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("uint32 y;"):]
        # cut_idx = generated_text.rfind("break;")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[:cut_idx + len("break;")]

    elif (vul_id == "EF10"):
        prepend = "\n".join(program_lines[:1685])
        append = "\n".join(program_lines[1707:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 1686, 1707)
        cut_idx = generated_text.find("sp->photometric = td->td_photometric;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("sp->photometric = td->td_photometric;"):]
        cut_idx = generated_text.rfind("return (1);")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx]
    
    elif (vul_id == "EF01"):
        # prepend = "\n".join(program_lines[:989])
        # append = "\n".join(program_lines[1015:])
        # code_block = extract_content_within_line_range (vulnerable_file_path, 990, 1016)
        # cut_idx = generated_text.find("for (col = 0; col < imagewidth; col += tw)")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[cut_idx :]
        # cut_idx = generated_text.rfind("if (col + tw > imagewidth)")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[:cut_idx]
        prepend = "\n".join(program_lines[:957])
        append = "\n".join(program_lines[1024:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 958, 1025)
        cut_idx = generated_text.find("uint16 bytes_per_sample;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx :]
        cut_idx = generated_text.rfind("if ((bps % 8) == 0)")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx]
    elif (vul_id == "EF02_01"):
        prepend = "\n".join(program_lines[:554])
        append = "\n".join(program_lines[576:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 555, 576)
        # print("code_block @@@@@@@@@@@@@@@@@@@@")
        # print(code_block)
        cut_idx = generated_text.find("int limit = tnh;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx :]
        cut_idx = generated_text.rfind("}")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + 1]
        # print("generated_text @@@@@@@@@@@@@@@@@@")
        # print(generated_text)
    elif (vul_id == "EF02_02"):
        prepend = "\n".join(program_lines[:116])
        append = "\n".join(program_lines[131:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 117, 131)
        # print("code_block @@@@@@@@@@@@@@@@@@@@")
        # print(code_block)
        cut_idx = generated_text.find("n &= 0x3f;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx :]
        cut_idx = generated_text.rfind("break;")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("break;")]
        # print("generated_text @@@@@@@@@@@@@@@@@@")
        # print(generated_text)

    elif (vul_id == "EF20"):
        prepend = "\n".join(program_lines[:486])
        append = "\n".join(program_lines[513:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 487, 513)
        print("code_block @@@@@@@@@@@@@@@@@@@@")
        print(code_block)
        cut_idx = generated_text.find("JDIMENSION row_width;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx :]
        cut_idx = generated_text.rfind("jpeg_calc_output_dimensions(cinfo);")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("jpeg_calc_output_dimensions(cinfo);")]
        # cut_idx = generated_text.rfind("}")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[:cut_idx + len("}")]
        print("generated_text @@@@@@@@@@@@@@@@@@")
        print(generated_text)
        
        # prepend = "\n".join(program_lines[:102])
        # append = "\n".join(program_lines[171:])
        # code_block = extract_content_within_line_range (vulnerable_file_path, 103, 171)
        # # print("code_block @@@@@@@@@@@@@@@@@@@@")
        # # print(code_block)
        # cut_idx = generated_text.find("JSAMPARRAY image_ptr;")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[cut_idx + len("JSAMPARRAY image_ptr;") :]
        # cut_idx = generated_text.rfind("}")
        # if (cut_idx >= 0):
        #     generated_text = generated_text[:cut_idx + len("}")]
        # print("generated_text @@@@@@@@@@@@@@@@@@")
        # print(generated_text)

    elif (vul_id == "EF22"):
        prepend = "\n".join(program_lines[:322])
        append = "\n".join(program_lines[353:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 323, 353)
        # print("code_block @@@@@@@@@@@@@@@@@@@@")
        # print(code_block)
        cut_idx = generated_text.find("cinfo->comps_in_scan = n;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("cinfo->comps_in_scan = n;") :]
        cut_idx = generated_text.rfind("cinfo->Ss = c;")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("cinfo->Ss = c;")]
        # print("generated_text @@@@@@@@@@@@@@@@@@")
        # print(generated_text)

    elif (vul_id == "EF18"):
        prepend = "\n".join(program_lines[:1174])
        append = "\n".join(program_lines[1202:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 1175, 1202)
        print("code_block @@@@@@@@@@@@@@@@@@@@")
        print(code_block)
        cut_idx = generated_text.find("case XML_ELEMENT_CONTENT_SEQ:")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("case XML_ELEMENT_CONTENT_SEQ:") :]
        cut_idx = generated_text.rfind("default:")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("default:")]
        print("generated_text @@@@@@@@@@@@@@@@@@")
        print(generated_text)

    elif (vul_id == "EF17"):
        prepend = "\n".join(program_lines[:4077])
        append = "\n".join(program_lines[4081:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 4078, 4081)
        print("code_block @@@@@@@@@@@@@@@@@@@@")
        print(code_block)
        cut_idx = generated_text.find("if (buf == NULL) goto mem_error;")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("if (buf == NULL) goto mem_error;") :]
        else:
            cut_idx = generated_text.find("goto mem_error;")
            if (cut_idx >= 0):
                generated_text = generated_text[cut_idx + len("goto mem_error;") :]
                idx = generated_text.find("if")
                if (idx >= 0):
                    generated_text = generated_text[cut_idx :]
        cut_idx = generated_text.rfind("buf[len] = 0;")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("buf[len] = 0;")]
        print("generated_text @@@@@@@@@@@@@@@@@@")
        print(generated_text)

    elif (vul_id == "EF15") :
        prepend = "\n".join(program_lines[:9834])
        append = "\n".join(program_lines[9855:])
        code_block = extract_content_within_line_range (vulnerable_file_path, 9836, 9855)
        print("code_block @@@@@@@@@@@@@@@@@@@@")
        print(code_block)
        cut_idx = generated_text.find("SKIP(2);")
        if (cut_idx >= 0):
            generated_text = generated_text[cut_idx + len("SKIP(2);") :]

        cut_idx = generated_text.rfind("GROW;")
        if (cut_idx >= 0):
            generated_text = generated_text[:cut_idx + len("GROW;")]
        print("generated_text @@@@@@@@@@@@@@@@@@")
        print(generated_text)
    
    write_file(responsepath, generated_text)
    write_file(ori_file_path, code_block)
    cmd_diff = "diff "+ori_file_path+" "+responsepath+ " > patchfile.patch"
    cmd_patch = "patch "+ori_file_path+" patchfile.patch"
    print("Executing command")
    execute_cmd_with_output(cmd_diff, project.working_project_dir)
    execute_cmd_with_output(cmd_patch, project.working_project_dir)
    con = read_file(ori_file_path)
    print("########################", ori_file_path)
    print(con)
    

    patch = prepend +"\n" + con + "\n"+ append

    #diff_str, cur_changed_line_cnt = print_diff(code_block, generated_text)


    return patch, ""
