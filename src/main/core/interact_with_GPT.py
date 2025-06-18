import openai
import time
import traceback
from main.utils.gpt_util import num_tokens_from_string
from main.utils.time_util import get_current_time
import random
from main.utils.csv_util import read_csv_with_header
from path_config import API_KEY_FILEPATH

MAX_HIT = 5
API_KEY_SET = read_csv_with_header(API_KEY_FILEPATH)  # add api key here

def interact_with_openai(model_name, prompt, temper):

    cur_api_idx = random.randint(0, len(API_KEY_SET) - 1)

    print("This prompt contains {} tokens for {} model".format(
        num_tokens_from_string(prompt, model_name), model_name), get_current_time())

    # Function for interacting with the API
    result = ""
    hit = 0
    while (hit < MAX_HIT):
        try:
            openai.organization = API_KEY_SET[cur_api_idx]['org']
            openai.api_key = API_KEY_SET[cur_api_idx]['api']
            response = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system",
                        "content": "You are a chatbot for vulnerablity repair."},
                    {"role": "user", "content": prompt},
                ],
                temperature=temper
            )
            for choice in response.choices:
                result += choice.message.content
            print("Returning the response")
            return result
        except Exception as e:
            print("Exception in interact_with_openai with key name {}".format(
                API_KEY_SET[cur_api_idx]['name']))
            traceback.print_exc()
            cur_api_idx = (cur_api_idx + 1) % len(API_KEY_SET)
            print("Try for another org", cur_api_idx)

        hit = hit + 1
        print("hit: ", hit)
        if (hit == len(API_KEY_SET)):
            time.sleep(200)

    # when something wrong with the API, the result can be empty
    if result == "":
        print("Failed to get response from OpenAI API.")
        return None

    return result
