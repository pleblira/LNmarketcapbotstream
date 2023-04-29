import boto3
from dotenv import load_dotenv, find_dotenv
import os
import json
from datetime import date, timedelta
import random

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

def s3_update_LN_capacity_and_compare(LN_capacity_in_BTC, automated):
    # creating dictionary to dump jsons in
    LN_capacity_by_day = []

    # today's date
    today_in_yyyymmdd = f"{date.today():%Y%m%d}"
    # downloading LN capacity history file from S3 bucket
    boto3.client('s3').download_file('pleblira', 'LN_capacity_by_day.json', 'assets/LN_capacity_by_day.json')

    # appending today's capacity to json file
    with open('assets/LN_capacity_by_day.json', 'r+') as openfile:
        LN_capacity_by_day = json.load(openfile)
        LN_capacity_by_day.append({"date":today_in_yyyymmdd,"capacity":LN_capacity_in_BTC})
        openfile.seek(0)
        openfile.write(json.dumps(LN_capacity_by_day, indent=4))

    # overwriting history file back to S3
    if automated == True:
        s3_upload = boto3.resource(
            's3',
            region_name='us-east-1',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        content=json.dumps(LN_capacity_by_day).encode('utf-8')
        s3_upload.Object('pleblira', 'LN_capacity_by_day.json').put(Body=content,ACL="public-read")

    # getting LN capacity from a week ago or a month ago
    random_weekly_or_monthly = random.randint(1,3)
    if random_weekly_or_monthly == 1:
        week_or_month = "last week"
        for value in LN_capacity_by_day:
            if value['date'] == f"{date.today() + timedelta(days=-7):%Y%m%d}":
                LN_capacity_in_BTC_from_previous_period = value['capacity']
    elif random_weekly_or_monthly == 2:
        week_or_month = "2 weeks ago"
        for value in LN_capacity_by_day:
            if value['date'] == f"{date.today() + timedelta(days=-14):%Y%m%d}":
                LN_capacity_in_BTC_from_previous_period = value['capacity']
    else:
        week_or_month = "last month"
        for value in LN_capacity_by_day:
            if value['date'] == f"{date.today() + timedelta(days=-30):%Y%m%d}":
                LN_capacity_in_BTC_from_previous_period = value['capacity']
        
    # checking if ATH for capacity
    LN_capacity_ATH = True
    for item in LN_capacity_by_day:
        if item['capacity'] > LN_capacity_in_BTC:
            LN_capacity_ATH = False

    LN_capacity_percentage_change = f"{(100 * (LN_capacity_in_BTC - int(LN_capacity_in_BTC_from_previous_period))/int(LN_capacity_in_BTC_from_previous_period)):+.2f}"
    LN_capacity_period_change_text = (f"LN capacity change from {week_or_month}: {LN_capacity_percentage_change.rstrip('0').rstrip('.')}%")
    print(LN_capacity_period_change_text)
    return LN_capacity_period_change_text, LN_capacity_ATH


if __name__ == '__main__':
    s3_update_LN_capacity_and_compare(3999)