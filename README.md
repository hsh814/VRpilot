# VRpilot
VRpilot: LLM-based Vulnerability Repair with Reasoning and Patch Validation Feedback 


# Setup 

  - Create a Python 3.11.2 virtual environment with all
    dependencies. Run the command: `$> bash create_venv.sh`
  - Install Docker Desktop version 4.14.0
  - Create extractfix images. Run the command: `$> bash download_extractfix_data.sh`
  - Or just run `$> cd ExtractFix_dataset && ./init.sh`
  - From the root directory:
    - Create file `openai_api.key` and add a key to access the openai API  
    - Run the following command `$> export PYTHONPATH="$PWD/src"`


# Note

  - Header of `openai_api.key`: 'name','org','api'

# Usage

  - rq1.py: Run this file to generate repair using CodexVR with ChatGPT
  - rq2.py: Run this file to generate repair using our proposed approach VRpilot
  - configurations folder contains the vulnerability information for each of the examples
  - utils folder contains utility scripts for VRpilot
  - project.py script contains methods for compiling and run test suite in specific docker containers
  - prompt.py script creates different types of prompts 
  - interact_with_GPT.py script contains method to query the LLM model with specific prompt

## VRpilot with VjBench Benchmark
All the scripts for running this dataset is available under llm_vul repository. 

N.B. Some of the scripts are taken from VjBench repository

  ### Dependency
  - Apache Maven 3.8.6
  - Java 8
  - Gradle 3.1

  ### Usage
  - set the following paths in llm_vul/scripts/util.py

    VUL4J_DIR: the absolute path to the folder containing the vulnerabiltiy projects from Vul4J

    VJBENCH_DIR: the absolute path the folder containing the vulnerabiltiy projects from VJBench
  - Setup Vul4J following the instructions in <a href="https://github.com/tuhh-softsec/vul4j" target="_blank">Vul4J repository</a>
  - Checkout Vul4J vulnerabilities following script at llm_vul/scripts/VUL4J/vul4j_projects.py
  - llm_vul/scripts/ChatGPT/rq2_vjBench.py: Run this file to run VRpilot on VjBench (15) vulnerabilities
  - llm_vul/scripts/ChatGPT/rq2_vul4j.py: Run this file to run VRpilot on Vul4j (35) vulnerabilities

