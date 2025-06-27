from main.utils.git_util import reset_repo
from main.utils.cmd_util import execute_cmd_with_output
from main.utils.file_util import copy_folder, delete_folder
from main.utils.docker_util import delete_image, build_image, check_image, run_with_new_src_code
import os
from path_config import TMP_DIR
import re
from main.utils.time_util import get_current_time


class Project():

    def __init__(self, vul_id, project_name, ori_project_dir, cur_com, docker_img_tag, exp_id):
        self.vul_id = vul_id
        self.project_name = project_name

        # original info about the project
        self.ori_project_dir = ori_project_dir
        self.ori_repo_dir = os.path.join(
            self.ori_project_dir,  "repos", project_name)
        self.cur_com = cur_com

        # information about the working project
        self.working_project_dir = os.path.join(
            TMP_DIR, f"{self.project_name}_{exp_id}")
        if os.path.exists(self.working_project_dir):
            delete_folder(self.working_project_dir)
        self.working_repo_dir = os.path.join(
            self.working_project_dir,  "repos", project_name)

        # information about docker
        self.container_id = None
        self.img_id = project_name  # set image name as project name
        self.img_tag = docker_img_tag

    def init_env(self):

        # copy the project to a tmp dir
        print("Copying {} to {}...".format(
            self.ori_project_dir, self.working_project_dir))
        if os.path.exists(self.working_repo_dir):
            delete_folder(self.working_repo_dir)
        copy_folder(self.ori_project_dir, self.working_project_dir)
        print("Done.")

        # reset
        if self.project_name != "potrace":
            print("Reseting the repo to {}...".format(self.cur_com))
            reset_repo(self.working_repo_dir, self.cur_com)
        print("Done.")

    def build(self):
        # init the docker environment
        print("[Time] start - build() image", get_current_time())
        exit_code, stdout_str, stderr_str = run_with_new_src_code(self.img_id, self.img_tag, self.working_repo_dir, f"/scripts/test_build.sh {self.vul_id}")
        print("[Time] end - build() image", get_current_time())
        output = stdout_str + "\n" + stderr_str
        for line in stderr_str.splitlines():
            if "error:" in line:
                return False, output
        return True, output

    def run_functional_test(self):
        print("[Time] start - run_functional_test()", get_current_time())
        num_of_test = 0
        num_of_passed = 0
        num_of_failed = 0
        error_msg = []

        exit_code, stdout_str, stderr_str = run_with_new_src_code(self.img_id, self.img_tag, self.working_repo_dir, f"/scripts/test_functionality.sh {self.vul_id}")
        # output = execute_cmd_with_output("docker run --rm {}:{} /scripts/test_functionality.sh {}".format(self.img_id, self.img_tag, self.vul_id), self.working_repo_dir)
        # print(output)
        output = stdout_str + "\n" + stderr_str

        if self.project_name == 'libxml2':
            # parse the result
            print("Parsing the result...")
            for line in output.splitlines():
                if line.startswith("Total") and "tests" in line and "errors" in line:
                    for tmp in line.split(","):
                        if "tests" in tmp:
                            num_of_test += (int)(
                                re.findall(r'\d+\.\d+|\d+', tmp)[0])
                        if "errors" in tmp:
                            if "no errors" not in line:
                                num_of_failed += (int)(
                                    re.findall(r'\d+\.\d+|\d+', tmp)[0])

            num_of_passed = num_of_test - num_of_failed

            if (num_of_failed > 0):
                lines = output.splitlines()
                i = 0
                while ((i + 1) < len(lines)):
                    if ("##" in lines[i] and "##" not in lines[i+1] and "Total" not in lines[i+1]):
                        error_msg.append(lines[i].replace("##", "").strip())
                    i = i + 1

        elif self.project_name == 'libtiff':
            lines = output.split('\n')

            if self.vul_id == "cve_2014_8128" or self.vul_id == "EF02_02":
                # remove ansi escape characters
                ansi_escape = re.compile(
                    r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
                for line in lines:
                    line = ansi_escape.sub('', line.strip())
                    if "# TOTAL: " in line:
                        num_of_test = (int)(line.strip().split("# TOTAL: ")[1])
                    elif "# PASS: " in line:
                        num_of_passed = (int)(
                            line.strip().split("# PASS: ")[1])

                num_of_failed = num_of_test - num_of_passed
                if (num_of_failed > 0) :
                    for line in lines:
                        line = ansi_escape.sub('', line.strip())
                        if "FAIL:" in line and "#" not in line:
                            error_msg.append(line.split(":")[1])
            else:
                for line in lines:
                    if 'Test' in line and ':' in line and '#' in line:
                        num_of_test += 1
                        if 'Passed' in line:
                            num_of_passed += 1
                        else:
                            num_of_failed += 1

        elif self.project_name == 'libjpeg-turbo':
            #print(output)
            lines = output.split('\n')
            if (self.vul_id == "cve_2018_19664"):
                for line in lines:
                    if 'Test' in line and ':' in line and '#' in line:
                        num_of_test += 1
                        if 'Passed' not in line:
                            num_of_failed += 1
                        else:
                            num_of_passed += 1
                # print(num_of_test, num_of_failed)
                if (num_of_failed > 0):
                    # i = lines.find("The following tests FAILED:")
                    i = 0
                    for line in lines:
                        if ("The following tests FAILED:" in line):
                            break
                        i += 1
                    i = i + 1
                    while (i < len(lines) - 4):
                        line = lines[i]
                        test_name = line[line.find(
                            "-")+1: line.find("(Failed")].strip()
                        error_msg.append(test_name)
                        i = i + 1

            elif (self.vul_id == "cve_2012_2806"):
                for line in lines:
                    if '->' in line and 'Done.' not in line:
                        num_of_test += 1
                        if 'Passed' in line:
                            num_of_passed += 1
                        else:
                            num_of_failed += 1

        print("[Time] end - run_functional_test()", get_current_time())
        return {'passed': num_of_passed, 'failed': num_of_failed, 'error_msg': error_msg, 'log': output}

    def run_security_test(self):
        """return True if the security test is passed, otherwise return False"""

        print("[Time] start - run_security_test()", get_current_time())
        exit_code, stdout_str, stderr_str = run_with_new_src_code(self.img_id, self.img_tag, self.working_repo_dir, f"/scripts/test_security.sh {self.vul_id}")
        # output = execute_cmd_with_output("docker run --rm {}:{} /scripts/test_security.sh {}".format(self.img_id, self.img_tag, self.vul_id), self.working_repo_dir)
        output = stdout_str + "\n" + stderr_str
        print(output)
        is_passed = True
        err_msg = None
        for line in stderr_str.splitlines():
            if not is_passed:
                err_msg += line
            if "ERROR:" in line: # AddressSanitizer
                print("Fail the security test.")
                is_passed = False
                err_msg = line
            if "runtime error:" in line: # UndefinedBehaviorSanitizer
                print("Fail the security test.")
                is_passed = False
                err_msg = line
        if not is_passed:
            print(f"Error message:\n{stderr_str}")
            err_msg = stderr_str
        return {"if_passed": is_passed, "error message": err_msg, "log": output}
        # if self.project_name == 'libxml2':

        #     # TODO: extract error msg from output
        #     if_passed = True
        #     err_msg = None

        #     # parse the result
        #     for line in output.splitlines():
        #         if "ERROR:" in line:
        #             print("Fail the security test.")
        #             if_passed = False
        #         if "SUMMARY:" in line:
        #             err_msg = line
        #             print("Security test error msg: ", err_msg)
        #             break

        #     return {"if_passed": if_passed, "error message": err_msg, 'log': output}

        # elif self.project_name == 'libtiff':

        #     # TODO: extract error msg from output
        #     if_passed = True
        #     err_msg = ""

        #     if self.vul_id == 'cve_2016_5321' or self.vul_id == 'cve_2016_10094':  # cve_2016_5321, cve_2016_5314, bugzilla_2633, cve_2016_10094 use ASAN
        #         for line in output.splitlines():
        #             if "ERROR:" in line:
        #                 print("Fail the security test.")
        #                 if_passed = False
        #                 err_msg += line
        #             if "SUMMARY:" in line:
        #                 err_msg += line
        #                 #print("Security test error msg: ", err_msg)
        #                 break
        #     elif self.vul_id == 'cve_2017_7601':  # cve_2017_7601-EF11 use UBSAN
        #         for line in output.splitlines():
        #             if "runtime error:" in line:
        #                 print("Fail the security test.")
        #                 if_passed = False
        #                 err_msg = line
        #                 break
        #     elif self.vul_id == 'cve_2016_3623' or self.vul_id == 'cve_2017_7595':  # cve_2017_7601-EF11 use UBSAN
        #         # remove ansi escape characters
        #         ansi_escape = re.compile(
        #             r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
        #         for line in output.splitlines():
        #             line = ansi_escape.sub('', line.strip())
        #             if "runtime error" in line:
        #                 print("Fail the security test.")
        #                 if_passed = False
        #                 err_msg += line + "\n"
        #                 #break
        #     elif self.vul_id == 'cve_2014_8128' or self.vul_id == 'EF02_02':  # EF02_* use ./configure and ASAN
        #         for line in output.splitlines():
        #             if "ERROR:" in line:
        #                 print("Fail the security test.")
        #                 if_passed = False
        #                 #break
        #             if "SUMMARY:" in line:
        #                 err_msg += line
        #                 #print("Security test error msg: ", err_msg)
        #                 break

        #     return {"if_passed": if_passed, "error message": err_msg, 'log': output}

        # elif self.project_name == 'libjpeg-turbo':

        #     # TODO: extract error msg from output
        #     if_passed = True
        #     err_msg = ""

        #     for line in output.splitlines():
        #         if "ERROR:" in line:
        #             print("Fail the security test.")
        #             if_passed = False
        #             #break
        #         if "SUMMARY:" in line:
        #             err_msg += line
        #             #print("Security test error msg: ", err_msg)
        #             break

        #     return {"if_passed": if_passed, "error message": err_msg, 'log': output}

    def run_test(self):
        fun_test_res = self.run_functional_test()
        sec_test_res = self.run_security_test()
        return fun_test_res, sec_test_res

    def inject_patch(self, filepath, patch):
        print("[Time] start - inject_patch()", get_current_time())
        target_filepath = os.path.join(self.working_repo_dir, filepath)
        with open(target_filepath, "w") as f:
            f.write(patch)
        print("[Time] end - inject_patch()", get_current_time())


def extract_err_msg_from_build_log(vul_file_rel_path, log, start_line_num, end_line_num):

    # include_line = []
    # control_error = "control reaches end of"
    # control_error_line = ""
    # for line_idx, line in enumerate(log.split("\n")):
    #     if vul_file_rel_path in line:
    #         include_line.append(line_idx)
    #     if control_error in line:
    #         control_error_line = line

    # if len(include_line) == 0:
    #     print("Error: cannot find the error message in the build log.")
    #     return "Unable to get build error"
    # # last_idx = len(include_line)
    # # if len(include_line) > 20 :
    # #     last_idx = 50
    # #     include_line = include_line[:last_idx]
    # #     if (control_error_line != ""):
    # #         include_line.append(control_error_line)
    # err_msg = '\n'.join(log.split("\n")[include_line[0]:include_line[-1]])

    # return err_msg
    program_lines = log.split("\n")
    control_error = "control reaches end of"
    line_regex = r'.c:([0-9]+):([0-9]+):'
    err_msg = ""
    i =0
    start = 0
    if ((start_line_num - 100)> 0):
        start = start_line_num - 100
    end =  end_line_num + 100
    total_line = 0
    while (i < len(program_lines)):
        line = program_lines[i]
        #print(line)
        if vul_file_rel_path in line:
            #print(line)
            match = re.search(line_regex, line)
            if match is not None:
                # print("Found match")
                #print(line)
                line_index, char_index = match.groups()
                line_index = int(line_index)
                if line_index >= start and line_index <= end:
                    err_msg += program_lines[i] +"\n" + program_lines[i+1]+"\n" + program_lines[i+2]+"\n"
                    i = i + 2
                    total_line = total_line + 1
            elif control_error in line:
                err_msg += program_lines[i] + "\n" + program_lines[i + 1] + "\n"
                i = i + 1
                total_line = total_line + 1
        if (total_line == 15):
            break
        i = i + 1
    return err_msg
