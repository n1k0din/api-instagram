import argparse
import os
import os.path
from pathlib import Path
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


def download_img(url, filename):
    full_path = f'{IMAGES_DIR}{filename}'

    response = requests.get(url, verify=False)
    response.raise_for_status()

    with open(full_path, 'wb') as file:
        file.write(response.content)


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
            os.remove(src_filepath)
            rgb_image.save(dst_filepath, format='JPEG')

        except Exception as e:
            print(e)


def post_images_to_instagram(bot, timeout=10):
    files = os.listdir(IMAGES_DIR)
    for file in files:
        img_path = f'{IMAGES_DIR}{file}'
        caption = 'another hubble image'

        bot.upload_photo(img_path, caption=caption)

        if bot.api.last_response.status_code != 200:
            print(bot.api.last_response)

        sleep(timeout)


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    resize_and_convert_images()

    login, password = get_login_password()

    bot = Bot()
    bot.login(username=login, password=password, ask_for_code=True)
    post_images_to_instagram(bot)


if __name__ == '__main__':
    main()
