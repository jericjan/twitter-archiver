# twitter-archiver
for archiving your twitter stuff, since twitter might go byebye soon

## Installation
1. Clone this repo
2. `pip install -r requirements.txt`

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

There are four options. These apply to both python files below:  
```
1.) Tweets and retweets  
2.) Likes  
3.) Bookmarks  
4.) Following
```
You can also run the files with an argument like so: `py main.py 1`  
This will automatically choose the first option.

### main.py
Run this to download JSONs containing your Twitter data

### downloader.py
Run this after main.py to download the media of the URLs inside those JSON files

### Note: This program will ask for **READ** access to your account but it will only do this once. All info is stored locally on your machine. `https://url-parameters-displayer.netlify.app/` is also exactly what it says. Feel free to check the source code if you don't believe me.
