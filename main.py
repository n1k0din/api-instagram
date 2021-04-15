import argparse
import os
import os.path
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from PIL import Image


IMAGES_DIR = 'images/'


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Постит картинки в инстач')
    parser.add_argument('login', help='логин в инстаграм')
    parser.add_argument('password', help='пароль в инстаграм')

    return parser


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
    _, filename = os.path.split(path)
    _, ext = os.path.splitext(filename)

    return ext


def resize_and_convert_images(width=1080):
    files = os.listdir(IMAGES_DIR)
    for file in files:
        src_filepath = f'{IMAGES_DIR}{file}'
        name, ext = os.path.splitext(file)
        dst_filepath = f'{IMAGES_DIR}{name}.jpg'

        try:
            image = Image.open(src_filepath)
            rgb_image = image.convert('RGB')
            rgb_image.thumbnail((width, width))
            rgb_image.save(dst_filepath, format='JPEG')

        except Exception as e:
            print(e)


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    args = create_argument_parser()

    resize_and_convert_images()


if __name__ == '__main__':
    main()
