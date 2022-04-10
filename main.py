import argparse
import os

import requests
from dotenv import load_dotenv
from urllib.parse import urlparse


def get_user_data(url, headers):
    url += '/v4/user'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['default_group_guid']


def create_bit_link(url, headers, long_url, group_guid, domain='bit.ly'):
    url += '/v4/shorten'
    data = {
        'long_url': long_url,
        'domain': domain,
        'group_guid': group_guid,
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def count_clicks(url, headers, bitlink):
    url += f'/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(url, headers, bitlink):
    url += f'/v4/bitlinks/{bitlink}'
    response = requests.get(url, headers=headers)
    if response.status_code == 403:
        raise requests.exceptions.HTTPError('Пользователь ввёл неверный битлинк')
    return response.ok


def is_valid(long_url):
    response = requests.get(long_url)
    response.raise_for_status()


def parse_argument():
    parser = argparse.ArgumentParser(description='Создание и проверка '
                                                 'Битлинков')
    parser.add_argument('--url', help='Ссылка или Битлинк')
    arg = parser.parse_args()
    return arg.url


if __name__ == '__main__':
    load_dotenv()
    api_token = os.environ['BITLY_API_TOKEN']
    domain = os.getenv('CUSTOM_DOMAIN')
    headers = {'Authorization': f'Bearer {api_token}'}
    url = 'https://api-ssl.bitly.com'
    try:
        group_guid = get_user_data(url, headers)
    except requests.exceptions.HTTPError:
        print('Пользователь ввёл неверный токен')
        raise
    long_url = parse_argument()
    if not long_url:
        long_url = input('Введите адрес сайта: ')
    if not long_url.startswith(('http://', 'https://')):
        long_url = 'https://' + long_url
    try:
        is_valid(long_url)
    except requests.exceptions.ConnectionError:
        print('Пользователь ввёл некорректную ссылку')
        raise
    bitlink = urlparse(long_url).hostname + urlparse(long_url).path
    if is_bitlink(url, headers, bitlink):
        total_clicks = count_clicks(url, headers, bitlink)
        print('Всего переходов по линку:', total_clicks)
    else:
        link = create_bit_link(url, headers, long_url, group_guid, domain)
        print('Битлинк', link['link'])
