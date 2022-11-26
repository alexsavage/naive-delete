# `naive-delete.py`

A script to quickly use the `data/tweets.js` file from your
[Twitter personal data archive](https://help.twitter.com/en/managing-your-account/accessing-your-twitter-data)
to delete your tweets.

## Prerequisites

1. You have used the Twitter Developer console to create:
   - An app with read/write permissions
   - OAuth v1 consumer keys
   - User tokens for yourself
2. You have downloaded your Twitter personal data archive, and it contains
   `data/tweets.js`

## Installation

1. Clone this repository
2. Use the tools of your choice to install the packages in `requirements.txt`.
3. Set up environment variables
   - (Recommended) Create a `.env` file with the following contents:

   ```env
   TW_CONSUMER_KEY=YourAppConsumerKey
   TW_CONSUMER_SECRET=YourAppConsumerSecret
   TW_ACCESS_TOKEN=YourAccountAccessToken
   TW_ACCESS_TOKEN_SECRET=YourAccountAccessTokenSecret
   ```

   - (Alternative) Set the above as actual environment variables.

## Usage

`naive-delete.py [-h] [--seek SEEK] [--logging {DEBUG,INFO,WARN,ERROR}] [infile]`

### Options

- `-h`, `--help`: show this help message and exit
- `--seek SEEK`: Number of tweets to skip ahead
- `--logging {DEBUG, INFO, WARN, ERROR}`: Logging verbosity level

### Positional arguments

- `infile`: path to tweets.js; read STDIN if omitted.

## Fairly Anticipated Questions

1. Why another tweet delete utility?
   - I participated in a really long thread that was confusing Semiphemeral as it tried to traverse up the thread, so I wanted to throw together something naive on my own.
   - I didn't look into other options before just coding.
2. How does it perform?
   - Running it on a Celeron laptop on home wi-fi, I was getting about 2 deletes per second.
   - I deleted about 11,000 tweets and it missed maybe three three old retweets.
3. Why does the code warn, but continue, on Forbidden or Not Found tweets?
   - The archive had some retweets that had either since been deleted, or the poster's account had been suspended or went private. So I couldn't interact with them via API.
4. I have an idea, will you accept a pull request?
   - Sure! But, I don't have any more tweets to delete, so I don't expect to test this a ton more.

## Dependencies

- [Tweepy](https://www.tweepy.org) to wrap the Twitter API and OAuth
- [json-stream](https://pypi.org/project/json-stream/) to parse JSON without reading the whole file into memory
- [python-dotenv](https://pypi.org/project/python-dotenv/) to store API keys and secrets outside the source code
