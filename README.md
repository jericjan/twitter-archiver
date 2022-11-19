# twitter-archiver
for archiving your twitter stuff, since twitter might go byebye soon

## Installation
1. Clone this repo
2. `pip install -r requirements.txt`
3. You also need [aria2](https://aria2.github.io/) installed

## Setting Up
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) and create a project
2. Set up User authentication settings
  - App permissions: `Read`
  - Type of App: `Confidential client`
  - App info:
    - Callback URI / Redirect URL: `https://url-parameters-displayer.netlify.app/` (it has to be this or it won't work)
    - Website URL: Just place any URL, preferably one that you own, but it doesn't matter too much.
3. Go to the **Keys and tokens** tab and you will find the Client ID and Client Secret of your app.
4. Create an `.env` file containing these two variables. Paste here the keys from the last step
```
CLIENT_ID="YOUR_CLIENT_ID_STRING_HERE"
CLIENT_SECRET="YOUR_CLIENT_SECRET_STRING_HERE"
```
5. Done!

## How To Use
Simply run `main.py` and follow the instructions. You can optionally provide arguments as shown below to run what you want immediately.

```
usage: main.py [-h] [-i [ENDPOINT] | -d [ENDPOINT]]

optional arguments:
  -h, --help            show this help message and exit
  -i [ENDPOINT], --info [ENDPOINT]
                        Downloads JSON info from selected endpoint
  -d [ENDPOINT], --download [ENDPOINT]
                        Downloads info from selected endpoint

ENDPOINT can be 'tweets', 'likes', 'bookmarks','following' or numbers 1-4 respectively.
```

### Note: This program will ask for **READ** access to your account but it will only do this once. All info is stored locally on your machine. `https://url-parameters-displayer.netlify.app/` is also exactly what it says. Feel free to check the source code if you don't believe me.
