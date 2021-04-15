# Публикация фоток от Хаббла в инстач
- `fetch_hubble.py` собирает фотки хаббла
- `fetch_spacex.py` собирает фотки spacex
- `main.py` конвертирует, изменяет размер и отправляет в инстаграм

## Установка

### Подготовка скрипта

1. Скачайте код и перейдите в папку проекта.
    ```bash
    git clone https://github.com/n1k0din/api-instagram.git
    ```  
    ```bash
    cd api-instagram
    ```
2. Установите вирт. окружение.
    ```bash
    python -m venv venv
    ```
3. Активируйте.
    ```bash
    venv\Scripts\activate.bat
    ```
    или
    ```bash
    source venv/bin/activate
    ```
4. Установите необходимые пакеты.
    ```bash
    pip install -r requirements.txt
    ```

## Запуск
```
python fetch_spacex.py
```

```
python fetch_hubble.py
```

```
python main.py instagram_login instagram_password
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
