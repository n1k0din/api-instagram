import requests
from pathlib import Path


IMAGES_DIR = 'images/'


def download_img(url, filename):
    full_path = f'{IMAGES_DIR}{filename}'

    response = requests.get(url)
    response.raise_for_status()

    with open(full_path, 'wb') as file:
        file.write(response.content)


def main():
    Path(IMAGES_DIR).mkdir(parents=True, exist_ok=True)

    filename = 'hubble.jpg'
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    download_img(url, filename)




if __name__ == '__main__':
    main()
