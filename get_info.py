import argparse
import json
import math
import time
import urllib.parse
from base64 import b64decode, b64encode
from pathlib import Path

import requests
from dotenv import dotenv_values

from UI import InputCode


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "choice",
        metavar="CHOICE",
        type=int,
        nargs="?",
        default=0,
        help="Your selected choice.",
    )
    args = vars(parser.parse_args())
    return args


def select_choice(args):
    endpoints = {1: "tweets", 2: "liked_tweets", 3: "bookmarks", 4: "following"}
    folders = {1: "tweets_retweets", 2: "likes", 3: "bookmarks", 4: "following"}
    if args["choice"] != 0:
        endpoint = endpoints[args["choice"]]
        folder = folders[args["choice"]]
        return endpoint, folder
    choice = input(
        "Select a number:\n"
        "1.) Tweets and retweets\n"
        "2.) Likes\n"
        "3.) Bookmarks\n"
        "4.) Following\n"
    )

    for x in folders.values():
        if not Path(x).exists():
            Path(x).mkdir()
        if not Path(x, "media").exists():
            Path(x, "media").mkdir()

    endpoint = endpoints[int(choice)]
    folder = folders[int(choice)]
    return endpoint, folder


def get_info(endpoint, folder):
    env = dotenv_values(".env")
    finished = False
    pagination_token = ""
    count = 1

    if endpoint == "following":
        parameters = "user.fields=id,name,profile_image_url,username,created_at"
    else:
        parameters = (
            "media.fields=url,type,preview_image_url,variants"
            "&expansions=attachments.media_keys,author_id"
            "&user.fields=name,created_at,id,username"
        )

    client_id = env["CLIENT_ID"]
    client_secret = env["CLIENT_SECRET"]

    refresh_token_file = Path("refresh_token.txt")
    if refresh_token_file.exists():
        refresh_token = b64decode(refresh_token_file.read_bytes()).decode("utf-8")
        print(f"refresh token is {refresh_token}")

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        data = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }

        response = requests.post(
            "https://api.twitter.com/2/oauth2/token",
            data=data,
            headers=headers,
            auth=(client_id, client_secret),
        )
        json_response = response.json()
        access_token = json_response.get("access_token")
        refresh_token = json_response.get("refresh_token")
        print(json_response)
        print(f"new refresh token is {refresh_token}")
        if refresh_token is None:
            print(f"FAIL:\n{response.text}")
        else:
            refresh_token_file.write_bytes(b64encode(refresh_token.encode("utf-8")))
    else:
        scopes = urllib.parse.quote(
            "tweet.read users.read follows.read offline.access space.read mute.read like.read list.read block.read bookmark.read"
        )
        redirect_uri = urllib.parse.quote_plus(
            "https://url-parameters-displayer.netlify.app/"
        )
        authorize_url = (
            "https://twitter.com/i/oauth2/authorize?"
            "response_type=code&"
            f"client_id={client_id}&"
            f"redirect_uri={redirect_uri}&"
            f"scope={scopes}"
            "&state=state&"
            "code_challenge=challenge&"
            "code_challenge_method=plain"
        )
        app = InputCode(css_path="styles.css")
        app.authorize_url = authorize_url
        code = app.run()
        # code = input("Give me the code in the URL after authorization: ")

        data = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": "https://url-parameters-displayer.netlify.app/",
            "code_verifier": "challenge",
        }

        response = requests.post(
            "https://api.twitter.com/2/oauth2/token",
            data=data,
            auth=(client_id, client_secret),
        )
        json_response = response.json()
        print(json_response)
        access_token = json_response.get("access_token")
        refresh_token = json_response.get("refresh_token")
        print(f"refresh token is {refresh_token}")
        refresh_token_file.write_bytes(b64encode(refresh_token.encode("utf-8")))

    user_id_file = Path("user_id.txt")
    if user_id_file.exists():
        with user_id_file.open(encoding="utf-8") as f:
            user_id = f.read()
    else:
        params = {"user.fields": "id"}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(
            "https://api.twitter.com/2/users/me", params=params, headers=headers
        )
        json_response = response.json()
        user_id = json_response["data"]["id"]
        with user_id_file.open("w", encoding="utf-8") as f:
            f.write(user_id)

    def get_num_of_file(f, endpoint):
        return int(f.name[len(endpoint) + 1 : -5])

    json_files = sorted(
        Path(folder).glob(f"{endpoint}_*.json"),
        key=lambda f: get_num_of_file(f, endpoint),
        reverse=True,
    )
    if json_files:
        last_file = json_files[0]
        count = get_num_of_file(last_file, endpoint)
        print(f"stopped at file {count}... continuing...")
        with last_file.open() as f:
            json_obj = json.load(f)
        try:
            pagination_token = json_obj["meta"]["next_token"]
            print("next token", pagination_token)
        except KeyError:
            print("Last page found. Exiting")
            finished = True
        count += 1
    while not finished:
        headers = {"Authorization": f"Bearer {access_token}"}
        url = (
            f"https://api.twitter.com/2/users/{user_id}/{endpoint}"
            "?max_results=100"
            f"&{parameters}"
        )
        url = (
            f"{url}&pagination_token={pagination_token}"
            if pagination_token != ""
            else url
        )
        r = requests.get(url, headers=headers)
        limit_remain = int(r.headers["x-rate-limit-remaining"])
        limit_reset = int(r.headers["x-rate-limit-reset"])
        if limit_remain <= 1:
            print("Close to hitting rate limit!")
            diff = limit_reset - math.floor(time.time())
            print(f"Sleeping for {diff} seconds")
            time.sleep(diff)
        if r.status_code != 200:
            print(f"FAIL.\n{r.text}")
            print(r.headers)
            break
        json_obj = r.json()
        with open(f"{folder}/{endpoint}_{count}.json", "w", encoding="utf-8") as f:
            json.dump(json_obj, f, indent=4)
        print(f"count: {count}")
        count += 1
        try:
            pagination_token = json_obj["meta"]["next_token"]
            print("next token", pagination_token)
        except KeyError:
            print("Last page found. Exiting")
            finished = True
