import tiktoken
import os
import time
import shutil

MODEL_MAX_TOKEN={'gpt-3.5-turbo':4000,'gpt-4-0314':8000}

def num_tokens_from_string(query: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(query))
    return num_tokens

def if_exceed_token_limit(query: str, model_name: str):
    """Returns True if the number of tokens in a text string exceeds the maximum allowed."""
    if model_name not in MODEL_MAX_TOKEN:
        raise ValueError(f"Model name {model_name} not supported.")
    max_tokens = MODEL_MAX_TOKEN[model_name]
    num_tokens = num_tokens_from_string(query, model_name)
    return num_tokens > max_tokens, num_tokens

def cut_query(query: str, model_name: str) -> str:
    """Cuts a query to the maximum number of tokens allowed by the model."""
    encoding = tiktoken.encoding_for_model(model_name)
    max_tokens = MODEL_MAX_TOKEN[model_name]
    num_tokens = len(encoding.encode(query))
    if num_tokens > max_tokens:
        query = encoding.decode(encoding.encode(query)[:max_tokens])
    return query

def write_file(filepath, content, create_dir=False):
    if create_dir:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)


def append_str_to_file(str, file_path):
    my_open = open(file_path, 'a')
    my_open.write(str)
    my_open.close()

def delete_folder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)

def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
