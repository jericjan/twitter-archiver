import argparse
import os
from pathlib import Path

from downloader import download
from get_info import get_info
from UI import ChooseOption, MainMenu


def choice_to_int(choice):
    print(choice)
    choices = ["tweets", "likes", "bookmarks", "following"]
    if choice.isdigit():
        return int(choice)
    if choice in choices:
        return choices.index(choice) + 1
    return 0


parser = argparse.ArgumentParser(
    epilog="ENDPOINT can be 'tweets', 'likes', 'bookmarks','following' or numbers 1-4 respectively."
)

group = parser.add_mutually_exclusive_group()
group.add_argument(
    "-i",
    "--info",
    metavar="ENDPOINT",
    choices=range(1, 5),
    nargs="?",
    help="Downloads JSON info from selected endpoint",
    type=choice_to_int,
)
group.add_argument(
    "-d",
    "--download",
    metavar="ENDPOINT",
    choices=range(1, 5),
    nargs="?",
    help="Downloads info from selected endpoint",
    type=choice_to_int,
)
args = vars(parser.parse_args())
gave_args = any(args.values())


if __name__ == "__main__":
    os.system("")
    if gave_args:
        if args["info"] is not None:
            choice1 = "info"
            choice2 = args["info"]
        else:
            choice1 = "download"
            choice2 = args["download"]
        print(choice1, choice2)
    else:
        app = MainMenu(css_path="styles.css")
        choice1 = app.run()
        app = ChooseOption(css_path="styles.css")
        choice2 = app.run()
        print(choice1, choice2)
    endpoints = {1: "tweets", 2: "liked_tweets", 3: "bookmarks", 4: "following"}
    folders = {1: "tweets_retweets", 2: "likes", 3: "bookmarks", 4: "following"}
    for x in folders.values():
        if not Path(x).exists():
            Path(x).mkdir()
        if not Path(x, "media").exists():
            Path(x, "media").mkdir()
    endpoint = endpoints[choice2]
    folder = folders[choice2]
    if choice1 == "info":
        get_info(endpoint, folder)
    else:
        download(endpoint, folder)
