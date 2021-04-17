import argparse
import logging
import os
import os.path
from pathlib import Path
from sys import exit
from time import sleep

import requests
from instabot import Bot
from PIL import Image


IMAGES_DIR = 'images/'


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Постит картинки в инстач')
    parser.add_argument('login', help='логин в инстаграм')
    parser.add_argument('password', help='пароль в инстаграм')

    return parser


def get_login_password():
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()
    login = args.login
    password = args.password

    return login, password


def download_img(url, filename, images_dir):
    full_path = f'{images_dir}{filename}'

    response = requests.get(url, verify=False)
    response.raise_for_status()

    with open(full_path, 'wb') as file:
        file.write(response.content)


def resize_and_convert_images(images_dir, width=1080):
    filenames = os.listdir(images_dir)
    for filename in filenames:
        src_filepath = f'{images_dir}{filename}'
        name, ext = os.path.splitext(filename)
        dst_filepath = f'{images_dir}{name}.jpg'

        try:
            image = Image.open(src_filepath)
            rgb_image = image.convert('RGB')
            rgb_image.thumbnail((width, width))
            os.remove(src_filepath)
            rgb_image.save(dst_filepath, format='JPEG')

        except IOError:
            logging.warning("Can't process image")


def post_images_to_instagram(bot, images_dir, caption, timeout=10):
    filenames = os.listdir(images_dir)
    for filename in filenames:
        img_path = f'{images_dir}{filename}'

        bot.upload_photo(img_path, caption=caption)

        if bot.api.last_response.status_code != 200:
            raise RuntimeError('Not OK response')

        sleep(timeout)


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    resize_and_convert_images(IMAGES_DIR)

    login, password = get_login_password()

    bot = Bot()
    bot.login(username=login, password=password, ask_for_code=True)

    try:
        caption = 'Just another space picture'
        post_images_to_instagram(bot, IMAGES_DIR, caption)
    except RuntimeError:
        exit(1)


if __name__ == '__main__':
    main()
