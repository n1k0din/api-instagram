import os
from urllib.parse import unquote, urlsplit

import requests

from main import download_img


def get_file_extension(file_url):
    unquoted_url = unquote(file_url)
    _, _, path, _, _ = urlsplit(unquoted_url)
    _, filename = os.path.split(path)
    _, ext = os.path.splitext(filename)

    return ext


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


if __name__ == '__main__':
    download_hubble_collection('spacecraft')
