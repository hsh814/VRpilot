import os
import shutil


def copy_folder(src, dst):
    shutil.copytree(src, dst)


def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)


def extract_content_within_line_range(filepath, startline, endline):
    """
    Extract the context within the line range.
    """
    context = ""
    with open(filepath, "r") as f:
        lines = f.readlines()
        for i in range(startline-1, endline):
            context += lines[i]
    return context


def read_file(filepath):
    """
    Read the content of the file.
    """
    with open(filepath, "r") as f:
        content = f.read()
    return content


def write_file(filepath, content, create_dir=False):
    if create_dir:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)


def append_str_to_file(str, file_path):
    my_open = open(file_path, 'a')
    my_open.write(str)
    my_open.close()