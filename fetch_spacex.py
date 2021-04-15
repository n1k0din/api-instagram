import requests

from main import download_img


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


if __name__ == '__main__':
    fetch_spacex_last_launch()
