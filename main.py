import os.path
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests


IMAGES_DIR = 'images/'


def download_img(url, filename):
    full_path = f'{IMAGES_DIR}{filename}'

    response = requests.get(url, verify=False)
    response.raise_for_status()

    with open(full_path, 'wb') as file:
        file.write(response.content)


def get_spacex_last_launch_photo_urls():
    url = 'https://api.spacexdata.com/v4/launches/latest'
    response = requests.get(url)
    response.raise_for_status()

    return response.json()['links']['flickr']['original']


def fetch_spacex_last_launch():
    urls = get_spacex_last_launch_photo_urls()

    filename_template = 'spacex{}.jpg'

    for num, photo_url in enumerate(urls, start=1):
        filename = filename_template.format(num)
        download_img(photo_url, filename)


def get_hubble_image_urls(image_id):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.get(url)
    response.raise_for_status()

    image_files = response.json()['image_files']
    return [f'https:{image_file["file_url"]}' for image_file in image_files]


def download_hubble_image(image_id):
    image_url = get_hubble_image_urls(image_id)[-1]
    ext = get_file_extension(image_url)
    filename = f'{image_id}{ext}'
    download_img(image_url, filename)


def download_hubble_collection(collection='all'):
    url = f'http://hubblesite.org/api/v3/images/{collection}'
    response = requests.get(url)
    response.raise_for_status()

    img_ids = [img['id'] for img in response.json()]

    for img_id in img_ids:
        print(f'downloading {img_id}...')
        download_hubble_image(img_id)


def get_file_extension(file_url):
    unquoted_url = unquote(file_url)
    _, _, path, _, _ = urlsplit(unquoted_url)
    _, tail = os.path.split(path)
    _, ext = os.path.splitext(tail)

    return ext


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    fetch_spacex_last_launch()

    download_hubble_collection(collection='spacecraft')


if __name__ == '__main__':
    main()
