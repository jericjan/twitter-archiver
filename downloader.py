import json
import subprocess
from pathlib import Path

from main import parse_args, select_choice

args = parse_args()
endpoint, folder = select_choice(args)

files = Path(folder).glob(f"{endpoint}_*.json")
media_folder = Path(folder, "media")
urls_to_dl = []


def file_is_downloaded(url):
    found = media_folder.glob(Path(url).name.split("?")[0])
    found = list(found)
    if not found:
        print(f"{Path(url).name} has not been downloaded!")
        return False
    return True


for file in files:
    print(f"Reading {file.name}")
    with file.open() as f:
        json_obj = json.load(f)
    if endpoint == "following":

        data = json_obj.get("data")
        if data:
            profile_urls = [x.get("profile_image_url") for x in data]
            for url in profile_urls:
                if not file_is_downloaded(url):
                    urls_to_dl.append(url)
        else:
            print("could not find 'data'. skipping.")
            continue
    else:
        try:
            medias = json_obj["includes"]["media"]
        except KeyError:
            print("could not find 'includes'. skipping.")
            continue
        for media in medias:
            if "url" in media:
                url = media["url"]

            else:
                variants = media["variants"]
                variants = sorted(
                    variants,
                    reverse=True,
                    key=lambda f: f["bit_rate"] if "bit_rate" in f else 0,
                )
                url = variants[0]["url"]

            if not file_is_downloaded(url):
                urls_to_dl.append(url)

if not urls_to_dl:
    print("There are no missing files to download. Yay!")
else:
    coms = ["aria2c", "-d", media_folder, "-Z", *urls_to_dl]
    process = subprocess.Popen(
        coms, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF-8"
    )
    outs, errs = process.communicate()
    print(outs)
    print(errs)
print("DONE!")
