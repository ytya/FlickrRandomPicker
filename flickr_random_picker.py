import csv
import time
from datetime import datetime
from pathlib import Path
from typing import Union

import fire
import numpy as np
import requests
from flickrapi import FlickrAPI
from tqdm import tqdm

import config


class FlickrRandomPicker:
    def __init__(self, config: config.Config):
        self.flickr = FlickrAPI(config.api_key, config.api_secret, format="parsed-json")
        self.min_timestamp = datetime(2004, 2, 10, 12, 0, 0).timestamp()  # Flickr release date
        self.timestamp_range = 12 * 60 * 60
        self.wait_time = config.wait_time
        self.retry_error_num = config.retry_error_num
        self.target_licenses = config.target_licenses
        self.search_extras = config.search_extras

        # Fetch license info
        license_info = self.flickr.photos.licenses.getInfo()
        self.licenses = {license["id"]: license for license in license_info["licenses"]["license"]}
        self.target_license_ids = ",".join(
            [license["id"] for license in self.licenses.values() if license["name"] in self.target_licenses]
        )

    def getLicense(self, id: int):
        return self.licenses.get(id)

    def fetchRandomDateSearch(self):
        # search by random dates (Flickr release date - Now)
        min_timestamp = (
            np.random.random() * ((time.time() - self.timestamp_range) - self.min_timestamp) + self.min_timestamp
        )
        max_timestamp = min_timestamp + self.timestamp_range
        result = self.flickr.photos.search(
            min_upload_date=int(min_timestamp),
            max_upload_date=int(max_timestamp),
            license=self.target_license_ids,
            **self.search_extras,
        )
        return result["photos"]["photo"]

    def pickRandomPhoto(self):
        # retry if fetching fails
        for _ in range(self.retry_error_num):
            time.sleep(self.wait_time)
            try:
                # search by random dates
                photos = self.fetchRandomDateSearch()
                if len(photos) == 0:
                    raise RuntimeError("can't find photos")
            except Exception as e:
                print(e)
                continue

            # fetch photo info
            for p in photos:
                time.sleep(self.wait_time * 2)
                photo_id = p["id"]
                try:
                    photo = self.flickr.photos.getInfo(photo_id=photo_id)["photo"]
                    sizes = self.flickr.photos.getSizes(photo_id=photo_id)["sizes"]
                    size = sorted(sizes["size"], key=lambda x: int(x["width"]), reverse=True)[0]
                except Exception:
                    continue
                return {"photo": photo, "size": size}
        return None


def random_pick(get_num: int = 100, output_csv: Union[str, Path] = "photos.csv"):
    try:
        picker = FlickrRandomPicker(config.Config())
    except Exception as e:
        print(e)
        print("Error: Init FlickrRandomPicker")
        exit()

    with open(output_csv, "w", encoding="utf8", newline="") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "id",
                "license",
                "owner",
                "url",
                "source",
                "rotation",
                "width",
                "height",
                "dateuploaded",
                "datetaken",
                "takeunknown",
            ],
            quotechar='"',
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()

        exist_ids = []

        for i in tqdm(range(get_num)):
            # fetch random photo
            photo = picker.pickRandomPhoto()
            if photo is None:
                print("Error: Can't get random photo")
                break
            photo, size = photo["photo"], photo["size"]

            # remove existed photo
            if photo["id"] in exist_ids:
                continue
            exist_ids.append(photo["id"])

            # write
            output_info = {
                "id": photo["id"],
                "license": picker.getLicense(photo["license"])["name"],
                "owner": photo["owner"]["username"],
                "url": photo["urls"]["url"][0]["_content"],
                "source": size["source"],
                "rotation": photo["rotation"],
                "width": size["width"],
                "height": size["height"],
                "dateuploaded": datetime.fromtimestamp(int(photo["dateuploaded"])),
                "datetaken": photo["dates"]["taken"],
                "takeunknown": photo["dates"]["takenunknown"],
            }
            writer.writerow(output_info)
            fp.flush()

    print(f"Total {len(exist_ids)} items")


def download(input_csv: Union[str, Path] = "photos.csv", output_dir: Union[str, Path] = "output"):
    # download photos according to input_csv
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(input_csv, "r", encoding="utf8") as fp:
        reader = csv.DictReader(fp)
        for row in tqdm(list(reader)):
            time.sleep(1)

            # fetch image
            url = row["source"]
            res = requests.get(url, timeout=(5, 30))
            if res.status_code != 200:
                print(f"can't download {url}")
                continue

            # save image
            filename = url.rsplit("/", 1)[-1]
            output_path = output_dir / filename
            with open(output_path, "wb") as fout:
                fout.write(res.content)


if __name__ == "__main__":
    fire.Fire()
