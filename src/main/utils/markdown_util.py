import re
from main.utils.file_util import read_file, write_file, extract_content_within_line_range
from path_config import CONFIG_DIR
import os
import json
from main.core.interact_with_GPT import interact_with_openai
from main.utils.cmd_util import execute_cmd_with_output
from main.data_structure.vulnerability import Vulnerability
from main.data_structure.project import Project

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

def make_patch_with_diff (vul: Vulnerability, project: Project, generated_text, idx):
    vul_code_file_rel_path = vul.vul_code_file_rel_path
    vul_id = vul.vul_id
    ori_file_path = os.path.join(project.working_project_dir,"temp_code_block.txt")
    responsepath = os.path.join(project.working_project_dir,"response_code_block.txt")
    vulnerable_file_path = os.path.join(project.working_repo_dir, vul_code_file_rel_path)
    content = read_file(vulnerable_file_path)
    program_lines = content.split("\n")
    # if (vul_id == "cve_2016_10094"):
    #     prepend = "\n".join(program_lines[:2885])
    #     append = "\n".join(program_lines[2930:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 2885, 2930)
    #     cut_idx = generated_text.find("unsigned char table_end[2];")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("unsigned char table_end[2];"):]
    #     cut_idx = generated_text.rfind("#endif")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("#endif")]
    # elif (vul_id == "cve_2017_7601"):
    #     prepend = "\n".join(program_lines[:1628])
    #     append = "\n".join(program_lines[1657:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 1625, 1657)
    #     cut_idx = generated_text.find("sp->v_sampling = td->td_ycbcrsubsampling[1];")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("sp->v_sampling = td->td_ycbcrsubsampling[1];"):]
    #     cut_idx = generated_text.rfind("break;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("break;")]
    # elif (vul_id == "cve_2016_3623"):
    #     # prepend = "\n".join(program_lines[:96])
    #     # append = "\n".join(program_lines[101:])
    #     # code_block = extract_content_within_line_range (vulnerable_file_path, 96, 101)
    #     # cut_idx = generated_text.find("case 'h':")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[cut_idx + len("case 'h':"):]
    #     # cut_idx = generated_text.rfind("break;")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[:cut_idx + len("break;")]
    #     prepend = "\n".join(program_lines[:252])
    #     append = "\n".join(program_lines[278:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 249, 278)
    #     cut_idx = generated_text.find("uint32 y;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("uint32 y;"):]
    #     # cut_idx = generated_text.rfind("break;")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[:cut_idx + len("break;")]

    # elif (vul_id == "cve_2017_7595"):
    #     prepend = "\n".join(program_lines[:1685])
    #     append = "\n".join(program_lines[1707:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 1686, 1707)
    #     cut_idx = generated_text.find("sp->photometric = td->td_photometric;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("sp->photometric = td->td_photometric;"):]
    #     cut_idx = generated_text.rfind("return (1);")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx]
    
    # elif (vul_id == "cve_2016_5321"):
    #     # prepend = "\n".join(program_lines[:989])
    #     # append = "\n".join(program_lines[1015:])
    #     # code_block = extract_content_within_line_range (vulnerable_file_path, 990, 1016)
    #     # cut_idx = generated_text.find("for (col = 0; col < imagewidth; col += tw)")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[cut_idx :]
    #     # cut_idx = generated_text.rfind("if (col + tw > imagewidth)")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[:cut_idx]
    #     prepend = "\n".join(program_lines[:957])
    #     append = "\n".join(program_lines[1024:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 958, 1025)
    #     cut_idx = generated_text.find("uint16 bytes_per_sample;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx :]
    #     cut_idx = generated_text.rfind("if ((bps % 8) == 0)")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx]
    # elif (vul_id == "cve_2014_8128"):
    #     prepend = "\n".join(program_lines[:554])
    #     append = "\n".join(program_lines[576:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 555, 576)
    #     # print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     # print(code_block)
    #     cut_idx = generated_text.find("int limit = tnh;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx :]
    #     cut_idx = generated_text.rfind("}")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + 1]
    #     # print("generated_text @@@@@@@@@@@@@@@@@@")
    #     # print(generated_text)
    # elif (vul_id == "EF02_02"):
    #     prepend = "\n".join(program_lines[:116])
    #     append = "\n".join(program_lines[131:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 117, 131)
    #     # print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     # print(code_block)
    #     cut_idx = generated_text.find("n &= 0x3f;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx :]
    #     cut_idx = generated_text.rfind("break;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("break;")]
    #     # print("generated_text @@@@@@@@@@@@@@@@@@")
    #     # print(generated_text)

    # elif (vul_id == "cve_2018_19664"):
    #     prepend = "\n".join(program_lines[:486])
    #     append = "\n".join(program_lines[513:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 487, 513)
    #     print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     print(code_block)
    #     cut_idx = generated_text.find("JDIMENSION row_width;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx :]
    #     cut_idx = generated_text.rfind("jpeg_calc_output_dimensions(cinfo);")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("jpeg_calc_output_dimensions(cinfo);")]
    #     # cut_idx = generated_text.rfind("}")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[:cut_idx + len("}")]
    #     print("generated_text @@@@@@@@@@@@@@@@@@")
    #     print(generated_text)
        
    #     # prepend = "\n".join(program_lines[:102])
    #     # append = "\n".join(program_lines[171:])
    #     # code_block = extract_content_within_line_range (vulnerable_file_path, 103, 171)
    #     # # print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     # # print(code_block)
    #     # cut_idx = generated_text.find("JSAMPARRAY image_ptr;")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[cut_idx + len("JSAMPARRAY image_ptr;") :]
    #     # cut_idx = generated_text.rfind("}")
    #     # if (cut_idx >= 0):
    #     #     generated_text = generated_text[:cut_idx + len("}")]
    #     # print("generated_text @@@@@@@@@@@@@@@@@@")
    #     # print(generated_text)

    # elif (vul_id == "cve_2012_2806"):
    #     prepend = "\n".join(program_lines[:322])
    #     append = "\n".join(program_lines[353:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 323, 353)
    #     # print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     # print(code_block)
    #     cut_idx = generated_text.find("cinfo->comps_in_scan = n;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("cinfo->comps_in_scan = n;") :]
    #     cut_idx = generated_text.rfind("cinfo->Ss = c;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("cinfo->Ss = c;")]
    #     # print("generated_text @@@@@@@@@@@@@@@@@@")
    #     # print(generated_text)

    # elif (vul_id == "cve_2017_5969"):
    #     prepend = "\n".join(program_lines[:1174])
    #     append = "\n".join(program_lines[1202:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 1175, 1202)
    #     print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     print(code_block)
    #     cut_idx = generated_text.find("case XML_ELEMENT_CONTENT_SEQ:")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("case XML_ELEMENT_CONTENT_SEQ:") :]
    #     cut_idx = generated_text.rfind("default:")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("default:")]
    #     print("generated_text @@@@@@@@@@@@@@@@@@")
    #     print(generated_text)

    # elif (vul_id == "cve_2012_5134"):
    #     prepend = "\n".join(program_lines[:4077])
    #     append = "\n".join(program_lines[4081:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 4078, 4081)
    #     print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     print(code_block)
    #     cut_idx = generated_text.find("if (buf == NULL) goto mem_error;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("if (buf == NULL) goto mem_error;") :]
    #     else:
    #         cut_idx = generated_text.find("goto mem_error;")
    #         if (cut_idx >= 0):
    #             generated_text = generated_text[cut_idx + len("goto mem_error;") :]
    #             idx = generated_text.find("if")
    #             if (idx >= 0):
    #                 generated_text = generated_text[cut_idx :]
    #     cut_idx = generated_text.rfind("buf[len] = 0;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("buf[len] = 0;")]
    #     print("generated_text @@@@@@@@@@@@@@@@@@")
    #     print(generated_text)

    # elif (vul_id == "cve_2016_1838") :
    #     prepend = "\n".join(program_lines[:9834])
    #     append = "\n".join(program_lines[9855:])
    #     code_block = extract_content_within_line_range (vulnerable_file_path, 9836, 9855)
    #     print("code_block @@@@@@@@@@@@@@@@@@@@")
    #     print(code_block)
    #     cut_idx = generated_text.find("SKIP(2);")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[cut_idx + len("SKIP(2);") :]

    #     cut_idx = generated_text.rfind("GROW;")
    #     if (cut_idx >= 0):
    #         generated_text = generated_text[:cut_idx + len("GROW;")]
    #     print("generated_text @@@@@@@@@@@@@@@@@@")
    #     print(generated_text)
    prepend = extract_content_within_line_range(vulnerable_file_path, 1, vul.vul_code_block_start_line - 1)
    code_block = extract_content_within_line_range(vulnerable_file_path, vul.vul_code_block_start_line, vul.vul_code_block_end_line)
    append = extract_content_within_line_range(vulnerable_file_path, vul.vul_code_block_end_line, len(program_lines))
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
