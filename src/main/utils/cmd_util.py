import subprocess

def execute_cmd_with_output(cmd, working_dir=None):
    try:
        print("Execute {} in {}".format(cmd, working_dir))
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir)
        
        output, error = process.communicate()
    except Exception as e:
        print("Execute {} failed! cwd={}".format(cmd, working_dir))
        print(error)
        return None
    return output.decode("ISO-8859-1") + "\n" + error.decode("ISO-8859-1")
