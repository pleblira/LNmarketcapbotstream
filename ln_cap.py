from amboss_get_LN_capacity import *
from coinmarketcap_get_btc_usd import *
from coinmarketcap_get_shitcoin_mcap import *
import random
import text_on_images
from create_gif import *
from s3_update_LN_capacity_and_compare import *

def LN_cap():
    # fetching LN capacity in BTC
    LN_capacity_in_BTC = amboss_get_LN_capacity()
    LN_capacity_text = f"Current LN capacity: {LN_capacity_in_BTC:.0f} BTC"

    # fetching BTC price in USD
    btc_usd = coinmarketcap_get_btc_usd()
    btc_usd_text =f"BTC price: ${btc_usd:,.0f}"

    # Calculating current amount allocated in the LN
    LN_mcap_text = f"$ allocated in the LN: ${LN_capacity_in_BTC*btc_usd:,.0f}"

    # commenting out all of the image stuff below
    # picking random image
    random_image_picker = random.randint(1,6)
    # random_image_picker = 1
    tweet_image = f"assets/blank_belly_dark_mode/{str(random_image_picker)}.jpg"

    # typing LN capacity on mascot
    tweet_image = text_on_images.image_draw_angled(LN_capacity_in_BTC, tweet_image)
    # subprocess.call(('open', "assets/tweet_image.jpg"))

    # making tweet image a gif with sparkle
    sparkle_gif_create_frames("assets/tweet_image.jpg", random_image_picker)

    # Getting the weekly increase based on the bot's history
    LN_capacity_period_change_text = s3_update_LN_capacity_and_compare(LN_capacity_in_BTC, automated=False)[0]

    # custom_text_yes_or_no = input("Would you like to add custom text to the tweet (y/n)? ")
    # if custom_text_yes_or_no == "y":
    #     custom_text = input("Type text (single line): ")

    # LIGHTNING NETWORK CAPACITY TWEET
    tweet_message = (
    "LIGHTNING NETWORK CAPACITY UPDATE" + "\n\n" + 
    LN_capacity_text + "\n" + 
    btc_usd_text + "\n" +
    LN_mcap_text
     + "\n" + "\n" +
    LN_capacity_period_change_text # move back inside of tweet_message in a week
        )
    # if custom_text_yes_or_no == "y":
    #     tweet_message = tweet_message + "\n\n" + custom_text
    print(tweet_message)
    # confirm_send_tweet = input("Send tweet (y/n)? ")
    # if confirm_send_tweet == "y":
    #     tweepy_send_tweet(tweet_message,"assets/tweet_image_sparkled.gif")
    #     print("Tweet sent")
    #     # os.remove("assets/tweet_image.jpg")
    #     quit()
    # else:
    return tweet_message
