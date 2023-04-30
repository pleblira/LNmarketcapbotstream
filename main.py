import tweepy
import os
from dotenv import load_dotenv, find_dotenv
import requests
import json
from datetime import datetime, timedelta
from bearer_oauth import *
from get_rules import *
from delete_all_rules import *
from set_rules import *
from create_throttle_list import *
from clean_up_and_save_recent_interactions import *
from get_exclude_reply_user_ids import *
from tweepy_send_tweet import *
from get_tweet_message import *
import time
from ln_cap import *
from ln_flippening_tracker import *

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")

throttle_time = 30

def get_stream(set):
    number_of_idle_pings = 0
    # print(f"number of idle pings: {number_of_idle_pings}")
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream?expansions=author_id,attachments.media_keys&media.fields=url", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code == 429:
        print("ran into error 429 so waiting for 30 seconds for connection to be reset")
        time.sleep(30)
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    if response.status_code != 200 and response.status_code != 429:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    
    for response_line in response.iter_lines():
        if response_line:
            number_of_idle_pings = 0
            print('setting number of idle pings to 0')
            json_response = json.loads(response_line)
            print(f"\n\n\n\n\n--- --- --- INCOMING TWEET --- --- ---\n")
            # print(f"the json dumps for json_response {json.dumps(json_response,indent=4)}\n\n")
            # checking if dollar amount included on stackjoin
            tweet_id = json_response["data"]["id"]
            tweet_message = json_response["data"]["text"]
            throttle_list = create_throttle_list(throttle_time)

            tweet_y = False
            tweet_n = False

            while not tweet_y and not tweet_n:
                for throttle_item in throttle_list:
                    print(f"\nthis is an item from throttle_list: {throttle_item}")
                    if json_response['data']['author_id'] in throttle_item:
                        print(f"the item id is {json_response['data']['author_id']}")
                        # print(f"the throttle list is {throttle_list}")
                        print("item found in throttle list, don't tweet")
                        tweet_n = True
                    else:
                        print(f"the item id is {json_response['data']['author_id']}")
                        print("not found in throttle list")
                if not tweet_n:
                    tweet_y = True
                print(f"tweet_y: {tweet_y}, tweet_n: {tweet_n}")
                print("\n")
            if tweet_y == True:
                print(json_response['data']['text'])
                if " cap" in json_response['data']['text'].lower().replace("lnmarketcapbot","").replace("capitalized","").replace("capital","").replace("mcap",""):
                    print("will tweet capacity")                
                    tweet_message = LN_cap()
                    tweet_image_path = "assets/tweet_image_sparkled.gif"
                    tweepy_send_tweet(tweet_message, tweet_id, json_response, tweet_image_path)
                    clean_up_and_save_recent_interactions(json_response, throttle_time)
                elif "compare" in json_response['data']['text'].lower():
                    prompt_message = json_response['data']['text'].lower()
                    prompt_parse_after_compare = prompt_message[8+prompt_message.find("compare"):]
                    if " " in prompt_parse_after_compare:
                        shitcoin = prompt_parse_after_compare[:prompt_parse_after_compare.find(" ")]
                    else:
                        shitcoin = prompt_parse_after_compare
                    query = LN_flippening_tracker(shitcoin.upper())
                    tweet_message = query[0]
                    tweet_image_path = query[1]
                    tweepy_send_tweet(tweet_message, tweet_id, json_response, tweet_image_path)
                    clean_up_and_save_recent_interactions(json_response, throttle_time)
                    pass
                else:
                    print("no recognized prompts")
                    # tweet_message = "no cap"
                # tweepy_send_tweet(tweet_message,tweet_id, json_response)
                pass
            else:
                print("tweet won't go out and cleaning up recent interactions was skipped")
        # number_of_idle_pings += 1
        # if number_of_idle_pings % 10 == 0:
        #     print(f'number of idle pings: {number_of_idle_pings}')
        # if number_of_idle_pings == 100:
        #     print('quitting')
        #     quit()

def main():
    rules = get_rules(bearer_oauth)
    delete_all_rules(rules, bearer_oauth)
    set = set_rules(bearer_oauth)
    get_stream(set)

if __name__ == "__main__":
    main()
    # clean_up_and_save_recent_interactions(json_response)