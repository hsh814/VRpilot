import docker
import traceback
from main.utils.cmd_util import execute_cmd_with_output
from main.utils.file_util import read_file
import os

def check_image(image_name, image_tag) -> bool:
    client = docker.from_env()
    return len(client.images.list(filters={'reference': f"{image_name}:{image_tag}"})) > 0

def delete_image(image_name, image_tag):
    client = docker.from_env()

    if client.images.list(name=f"{image_name}:{image_tag}"):
        client.images.remove(f"{image_name}:{image_tag}", force=True)
        print(f"Image {image_name}:{image_tag} removed successfully.")
    else:
        print(f"Image {image_name}:{image_tag} does not exist, skip removing.")



def build_image(image_name, image_tag, working_repo_dir, vul_id):

    if_build_success = True
    log = None

    # Build the image with the specified tag
    try:
        cmd = f"docker build -t {image_name}:{image_tag} --build-arg ID=\"{vul_id}\" . > build.log 2>&1"
        output = execute_cmd_with_output(cmd, working_repo_dir)
        log = read_file(os.path.join(working_repo_dir, "build.log"))
        
    except Exception as e:
        print(f"Failed to build image {image_name}:{image_tag}, error: {e}")

    for line in log.split("\n"):
        if "error:" in line:
            if_build_success = False
            break
    return if_build_success, log

def clear_all_docker_containers():
    client = docker.from_env()

    docker_containers = client.containers.list(all=True)
    # for dc in docker_containers:
    #     dc.remove(force=True)

    # docker_img = client.images.list(all=True)
    # for di in docker_img:
    #     di.remove(force=True)   
    
