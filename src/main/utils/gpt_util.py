import tiktoken

MODEL_MAX_TOKEN={'gpt-3.5-turbo':4000,'gpt-4-0314':8000, 'gpt-4o-mini': 2000000, 'gpt-4o': 100000, 'o3-2025-04-16': 100000}

def num_tokens_from_string(query: str, model_name: str) -> int:
    """Returns the number of tokens in a text string."""
    if model_name == "o3-2025-04-16":
        encoding = tiktoken.get_encoding("cl100k_base")
    else:
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
