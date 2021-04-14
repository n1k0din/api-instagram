import requests
from pathlib import Path


def main():
    Path("images/").mkdir(parents=True, exist_ok=True)

    filename = 'images/hubble.jpg'
    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    response = requests.get(url)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    main()
