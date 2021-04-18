import requests
import urllib3

from main import download_img
from main import IMAGES_DIR


def get_spacex_last_launch_photo_urls():
    url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()['links']['flickr']['original']


def fetch_spacex_last_launch(images_dir):
    urls = get_spacex_last_launch_photo_urls()

    filename_template = 'spacex_{}.jpg'

    for num, photo_url in enumerate(urls, start=1):
        filename = filename_template.format(num)
        download_img(photo_url, filename, images_dir)


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    fetch_spacex_last_launch(IMAGES_DIR)
