import requests
from pathlib import Path


IMAGES_DIR = 'images/'


def download_img(url, filename):
    full_path = f'{IMAGES_DIR}{filename}'

    response = requests.get(url)
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


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
