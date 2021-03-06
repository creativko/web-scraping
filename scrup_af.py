import requests
import json
import config
from bs4 import BeautifulSoup
from datetime import datetime


DATE_NOW = str(datetime.now())


def json_writen(data, name):
    with open(f'{name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)


def query_paginate(link: str) -> list:
    """Получаем все страницы с пагинацией"""
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    page_list = soup.find_all('span', {'class': 'pagelist'})
    link_list = f'{link}?page='
    result = [link_list + item.get_text() for item in page_list]
    return result


def query_page(link: str, category: int):
    """Данные с одной страницы"""
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    result = soup.find_all('div', {'class': 'center_live'})
    result_author = soup.select("div.center_live span")
    count = len(result_author)
    response = []
    counter = 0
    for item in range(len(result)):
        new_str = str(result[item].get_text()).strip()
        try:
            new_author = str(result_author[counter].get_text()).strip()
            text = new_str[:-len(new_author)]
        except IndexError as error:
            print(f'{error} - нету автора! - {text}')
        response.append({
            'model': config.MODEL,
            'fields': {
                'content': text,
                'author': new_author,
                'category': category,
                'time_create': DATE_NOW,
                'time_update': DATE_NOW
            }
        })
        counter += 1
        if counter > count:
            break
    return response


while True:
    url = str(input('Введите URL '))
    cat_id = int(input('Введите категорию '))
    file_name = str(input('Введите название файла '))
    parse_off = int(input('Продолжать работу? '))
    page = query_paginate(url)
    all_data = []
    for link_query in page:
        q = query_page(link_query, cat_id)
        all_data.extend(q)
    json_writen(all_data, file_name)
    if parse_off == 0:
        break
