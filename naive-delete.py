import argparse
from dotenv import load_dotenv
import io
import json_stream
import logging
import os
import sys
import tweepy

input: io.TextIOWrapper
seek: int
count = 0

parser = argparse.ArgumentParser(description='Delete your tweets')

parser.add_argument(
    'infile',
    nargs='?',
    type=argparse.FileType('r', encoding='utf-8'),
    default=sys.stdin,
    help='path to tweets.js'
)

parser.add_argument(
    '--seek',
    type=int,
    required=False,
    default=0,
    help='Number of tweets to skip ahead'
)

parser.add_argument(
    '--logging',
    type=str,
    choices=['DEBUG', 'INFO', 'WARN', 'ERROR'],
    required=False,
    default='WARN',
    help="Logging verbosity level"
)

args = parser.parse_args()
input = args.infile
seek = args.seek

load_dotenv()

api = tweepy.API(
    auth=tweepy.OAuth1UserHandler(
        consumer_key=os.environ.get("TW_CONSUMER_KEY"),
        consumer_secret=os.environ.get("TW_CONSUMER_SECRET"),
        access_token=os.environ.get("TW_ACCESS_TOKEN"),
        access_token_secret=os.environ.get("TW_ACCESS_TOKEN_SECRET"),
        callback="x-placeholder-callback://dev/null"
    ),
    wait_on_rate_limit=True
)

logging.basicConfig(
    level=args.logging,
    format='%(asctime)s %(levelname)s %(message)s')

try:
    logging.debug("Verifying credentials")
    api.verify_credentials()
    logging.info("Credentials verified")
except Exception as e:
    logging.error("Cannot verify credentials", exc_info=e)
    exit(255)

logging.debug("Skip non-JSON header")
input.seek(25)  # advance stream past non-JSON header

logging.debug("Begin parsing as json_stream")
stream = json_stream.load(input)

for record in stream:
    count = count+1
    logging.debug("Start record #" + count)
    tweet_id = record["tweet"]["id"]
    if seek > 0:
        logging.debug("Seeking ahead " + seek)
        seek = seek-1
    else:
        try:
            logging.debug("Deleting #" + count + " " + tweet_id)
            api.destroy_status(tweet_id)
            logging.info("Deleted #" + count + " " + tweet_id)
        except tweepy.Forbidden:
            logging.warning("Forbidden: #" + count + " " + tweet_id)
        except tweepy.NotFound:
            logging.warning("Not found: #" + count + " " + tweet_id)
        except Exception as e:
            logging.error("Unhandled exception: #" +
                          count + " " + tweet_id, exc_info=e)
            break
print(count)
