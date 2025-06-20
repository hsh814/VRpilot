import docker
import traceback
from main.utils.cmd_util import execute_cmd_with_output
from main.utils.file_util import read_file
import os
import io
import tarfile

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



def build_image(image_name, image_tag, working_repo_dir):
    
    client = docker.from_env()
    log_lines = list()

    # Build the image with the specified tag
    log_file = open(os.path.join(working_repo_dir, "docker-image-build.log"), "w", encoding='utf-8')
    try:
        print(f"[*] Building image {image_name}:{image_tag} from {working_repo_dir}")
        image, build_log_generator = client.images.build(path=working_repo_dir, tag=f"{image_name}:{image_tag}", rm=True, forcerm=True)
        for chunk in build_log_generator:
            if 'stream' in chunk:
                line = chunk['stream'].strip()
                if line != "":
                    print(line)
                    log_lines.append(line)
                    log_file.write(line + '\n')
        print(f"[*] Successfully build image {image.short_id}")
        return True, "\n".join(log_lines)
    except docker.errors.BuildError as e:
        print("\n[!] Failed to build image. Capturing error log...")
        
        for line_info in e.build_log:
            if 'stream' in line_info:
                line = line_info['stream'].strip()
                if line:
                    print(line)
                    log_lines.append(line)
                    log_file.write(line + '\n')

        return False, "\n".join(log_lines)
    except Exception as e:
        print(f"Failed to build image {image_name}:{image_tag}, error: {e}")
        log_file.write(f"Error msg: {e}\n")
        return False, "\n".join(log_lines)
    finally:
        log_file.close()

def clear_all_docker_containers():
    client = docker.from_env()

    docker_containers = client.containers.list(all=True)
    # for dc in docker_containers:
    #     dc.remove(force=True)

    # docker_img = client.images.list(all=True)
    # for di in docker_img:
    #     di.remove(force=True)   

# working_repo_dir = "ExtractFix_dataset/docker/libtiff/repos/libtiff"
def run_with_new_src_code(image_name, image_tag, working_repo_dir, cmd): 
    client = docker.from_env()
    container = client.containers.create(f"{image_name}:{image_tag}", detach=True, command=["sleep", "infinity"])
    container.start()
    tarstream = io.BytesIO()
    with tarfile.open(fileobj=tarstream, mode='w') as tar:
        tar.add(working_repo_dir, arcname=os.path.basename(working_repo_dir))
    tarstream.seek(0)
    container.put_archive("/dataset/repos", tarstream)
    
    exit_code, (stdout, stderr) = container.exec_run(cmd, demux=True)
    container.remove(force=True)
    stdout_str = stdout.decode('utf-8', errors='ignore').strip() if stdout else ""
    stderr_str = stderr.decode('utf-8', errors='ignore').strip() if stderr else ""
    return exit_code, stdout_str, stderr_str
    