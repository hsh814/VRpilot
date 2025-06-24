from main.utils.docker_util import run_with_new_src_code, check_image, build_image, delete_image
from main.utils.git_util import get_parent_commit, reset_repo
import path_config
import main.utils.json_util
import os

projects = ["binutils-gdb", "coreutils", "jasper", "libjpeg-turbo", "libming", "libtiff", "libxml2", "zziplib"]
for project in projects:
  project_dir = os.path.join(path_config.DATA_DIR, "docker", project)
  repo_dir = os.path.join(project_dir, "repos", project)
  delete_image(project, "default")
  if not check_image(project, "default"):
    print(f"[{project}] build image")
    is_success, build_log = build_image(project, "default", project_dir)
    if not is_success:
      print(f"[{project}] docker build error!!!!")
      continue
        
  configs = main.utils.json_util.read_json_from_file(os.path.join("/home/shhan/code/VRpilot/configurations", project, "configuration.json"))
  for config in configs["configurations"]:
    vul_id = config["vul_id"]
    fix_commit = config["fix_commit"]
    target_commit = get_parent_commit(repo_dir, fix_commit)
    print(f"{project} - {vul_id}: found commit {fix_commit} - {target_commit}")
    reset_repo(repo_dir, target_commit)
    print(f"[{project} - {vul_id}] ############")
    exit_code, stdout_str, stderr_str = run_with_new_src_code(project, "default", repo_dir, f"/scripts/test_security.sh {vul_id}")
    print(f"exit_code: {exit_code}\n{stdout_str}\n{stderr_str}")
    print(f"[{project} - {vul_id}] ############ Finished!!!!")
        
  