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


def query_page_author(link: str):
    """Данные с одной страницы"""
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    result = soup.select(f'div.center_live span')
    response = [item.get_text().strip() for item in result]
    return response


def query_page_dict(link: str, category: int):
    """Данные с одной страницы"""
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    result = soup.select(f'div.center_live')
    response = []
    for item in range(len(result)):
        response.append({
            'model': config.MODEL,
            'fields': {
                'content': result[item].get_text().strip(),
                'author': '',
                'category': category,
                'time_create': DATE_NOW,
                'time_update': DATE_NOW
            }
        })
    return response


while True:
    url = str(input('Введите URL '))
    cat_id = int(input('Введите категорию '))
    file_name = str(input('Введите название файла '))
    parse_off = int(input('Продолжать работу? '))
    page = query_paginate(url)
    list_content = []
    list_author = []
    for link_query in page:
        content_list = query_page_dict(link_query, cat_id)
        author_list = query_page_author(link_query)
        author_list = list(set(author_list))
        list_content.extend(content_list)
        list_author.extend(author_list)
    for index in range(len(list_content)):
        for author in list_author:
            if author in list_content[index]['fields']['content']:
                list_content[index]['fields']['content'] = list_content[index]['fields']['content'][:-len(author)]
                list_content[index]['fields']['author'] = author

    json_writen(list_content, file_name)
    if parse_off == 0:
        break
