from amboss_get_LN_capacity import *
from coinmarketcap_get_btc_usd import *
from coinmarketcap_get_shitcoin_mcap import *
import random
import text_on_images
from create_gif import *
from s3_update_LN_capacity_and_compare import *

def LN_flippening_tracker(shitcoin):
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = f"LN channel capacity: {str(LN_capacity_in_BTC)} BTC"

    # fetching BTC price in USD
    btc_usd = coinmarketcap_get_btc_usd()
    btc_usd_text =f"BTC price: ${btc_usd:,.0f}"

    # Calculating current amount allocated in the LN
    LN_mcap_text = f"$ allocated in the LN: ${LN_capacity_in_BTC*btc_usd:,.0f}"

    # fetching shitcoin mcap
    # shitcoin = input("What shitcoin would you like to compare LN to? ").upper()
    # coinmarketcap_get_shitcoin_mcap(shitcoin)
    shitcoin = shitcoin.replace("$","")
    shitcoin_mcap = coinmarketcap_get_shitcoin_mcap(shitcoin)[1]
    if shitcoin_mcap == 123456789:
        tweet_message = "Shitcoin not found, try again."
        tweet_image_path = "assets/blank_belly_dark_mode/4.jpg"
        return tweet_message, tweet_image_path
    shitcoin_mcap_text = f"{shitcoin.upper()} market cap: ${shitcoin_mcap:,.0f}"
    
    # Comparing LN network with shitcoin
    percentage_bar = int(LN_capacity_in_BTC*btc_usd/shitcoin_mcap*100/5)
    if percentage_bar > 20:
        percentage_bar = 20
    percentage_calculation = str(f"{LN_capacity_in_BTC*btc_usd/shitcoin_mcap*100:.2f}%")
    if float(percentage_calculation.replace("%","")) > 100:
        percentage_calculation = percentage_calculation.replace("%","")
        percentage_calculation = f"FLIPPENED (LN market cap = {float(percentage_calculation)/100:.2f}X ${shitcoin.upper()}'s market cap)"

    flippening_progress_text = (
        "Progress (LN flippening " + shitcoin + ")\n" + 
        "▓" * percentage_bar + "░" * (20 - percentage_bar) + " " +
        percentage_calculation
    )

    # asking if would like to choose image or pick a random one
    # random_image_or_pick = input("Pick and image or choose at random (pick/random)? ")
    random_image_or_pick = "random"
    if random_image_or_pick == "pick":
        image_url_or_path = input("insert image full URL or path here: ")
        # if image_url_or_path.find("http")>-1 and image_url_or_path.find("//")>0:
        #     urllib.request.urlretrieve(image_url_or_path, "assets/00000001.jpg")
        #     tweet_image = "assets/00000001.jpg"
        # else:
        #     tweet_image = image_url_or_path
    elif random_image_or_pick == "random":
        random_image_picker = random.randint(1,5)
        tweet_image_path = "assets/full_belly_dark_mode/" + str(random_image_picker) + ".png"
    else:
        print("Wrong option detected")
        quit()
    # subprocess.call(('open', tweet_image))
    

    # custom_text_yes_or_no = input("Would you like to add custom text to the tweet (y/n)? ")
    # if custom_text_yes_or_no == "y":
    #     custom_text = input("Type text (single line): ")

    # LIGHTNING NETWORK FLIPPENING TRACKER TWEET
    tweet_message = (
    "LIGHTNING FLIPPENING TRACKER - LN vs $" + shitcoin + "\n\n" + 
    LN_capacity_text + "\n" + 
    btc_usd_text + "\n" + 
    LN_mcap_text + "\n\n" + 
    shitcoin_mcap_text + "\n\n" + 
    flippening_progress_text
    )
    # if custom_text_yes_or_no == "y":
    #     tweet_message = tweet_message + "\n\n" + custom_text
    print(tweet_message)
    return tweet_message, tweet_image_path
    # confirm_send_tweet = input("Send tweet (y/n)? ")
    # if confirm_send_tweet == "y":
    #     tweepy_send_tweet(tweet_message,tweet_image)
    #     print("Tweet sent")
    #     if random_image_or_pick == "pick" and image_url_or_path.find("http")>-1 and image_url_or_path.find("//")>0:
    #         os.remove("assets/00000001.jpg")
    #     quit()
    # else:
        # return
