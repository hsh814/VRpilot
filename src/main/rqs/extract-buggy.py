from main.utils.docker_util import run_with_new_src_code, check_image, build_image, delete_image
from main.utils.git_util import get_parent_commit, reset_repo
import path_config
import main.utils.json_util
import os
import re

projects = ["binutils-gdb", "coreutils", "ffmpeg", "jasper", "libjpeg-turbo", "libming", "libtiff", "libxml2", "potrace", "zziplib"]
for project in projects:
  project_dir = os.path.join(path_config.DATA_DIR, "docker", project)
  repo_dir = os.path.join(project_dir, "repos", project)
  configs = main.utils.json_util.read_json_from_file(os.path.join("configurations", project, "configuration.json"))
  for config in configs["configurations"]:
    vul_id = config["vul_id"]
    fix_commit = config["fix_commit"]
    if project != "potrace":
      target_commit = get_parent_commit(repo_dir, fix_commit)
      print(f"{project} - {vul_id}: found commit {fix_commit} - {target_commit}")
      # reset_repo(repo_dir, target_commit)
    result_dir = os.path.join(path_config.DATA_DIR, "buggy", project, vul_id)
    os.makedirs(result_dir, exist_ok=True)
    # os.system(f"cp {repo_dir}/{config['vul_code_file_rel_path']} {result_dir}")
    print(f"cp {repo_dir}/{config['vul_code_file_rel_path']} {result_dir}")
    
    patch_result_file = os.path.join("result", "RQ2", vul_id, f"{project}{vul_id}", "new", "result.txt")
    patch_dir = os.path.join("result", "RQ2", vul_id, f"{project}{vul_id}", "new", "patch")
    
    if not os.path.exists(patch_result_file):
      print(f"[{vul_id}] result.txt not found. Skipping.")
      continue
    if not os.path.exists(patch_dir):
      print(f"[{vul_id}] patch directory not found. Skipping.")
      continue

    files = os.listdir(patch_dir)

    correct_patch_indices = set()
    with open(patch_result_file, 'r') as f:
      for line in f:
        if "Correct response found" in line:
          match = re.search(r"iteration (\d+), query idx (\d+)", line)
          if match:
            iteration = match.group(1)
            query_idx = match.group(2)
            correct_patch_indices.add((iteration, query_idx))

    if not correct_patch_indices:
      print(f"[{vul_id}] No correct patches found in result.txt.")
      continue

    print(f"[{vul_id}] Found correct indices: {correct_patch_indices}")

    found_patches = []
    patch_pattern = re.compile(r"temp_1_itr_(\d+)_query_(\d+).*")

    for filename in files:
      if filename.endswith(".diff"):
        continue
      match = patch_pattern.match(filename)
      if match:
        iteration = match.group(1)
        query_idx = match.group(2)
        
        if (iteration, query_idx) in correct_patch_indices:
          found_patches.append(filename)

    print(f"[{project} - {vul_id}] Matched correct patch files: {found_patches}")
    for patch in found_patches:
      os.system(f"diff {result_dir}/{os.path.basename(config['vul_code_file_rel_path'])} {patch_dir}/{patch} > {result_dir}/{patch}.diff")
  