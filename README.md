# Обрезка ссылок с помощью Bitly.com

Проект создан для автоматизации процесса создания коротких ссылок через сервис http://bitly.com/

### Как установить

Для запуска проекта Вам необходим .env-файл со следующим содержанием:
```
BITLY_API_TOKEN=
CUSTOM_DOMAIN=bit.ly
```
BITLY_API_TOKEN - Ваш токен на сайте http://bitly.com/

CUSTOM_DOMAIN - Ваш домен для персонализации ссылок (при наличии)

Python3 должен быть уже установлен. 
Рекомендуется использовать
[virtualenv/venv](https://docs.python.org/3/library/venv.html).
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
Для запуска проекта по умолчанию:
```
python main.py
```
Для запуска проекта с ключом `url`:
```
python main.py --url https://dvmn.org/
```


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

