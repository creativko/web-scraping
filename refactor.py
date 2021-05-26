import requests
import json
import config
import unicodedata
from bs4 import BeautifulSoup
from datetime import datetime


DATE_NOW = str(datetime.now())


def json_writen(data, name):
    with open(f'{name}.json', 'w') as json_file:
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
    response = []
    for item in result:
        new_author = item.get_text()
        new_author = unicodedata.normalize('NFKD', new_author)
        new_author = new_author.strip()
        response.append(new_author)
    return response


def query_page_dict(link: str, category: int):
    """Данные с одной страницы"""
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    result = soup.find_all('div', {'class': 'center_live'})
    response = []
    for item in range(len(result)):
        content = result[item].get_text()
        content = unicodedata.normalize('NFKD', content)
        content = content.strip()
        content = content.replace('\"', '')
        content = content.replace('»', '')
        content = content.replace('\n', ' ')
        response.append({
            'model': config.MODEL,
            'fields': {
                'content': content,
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
        list_content.extend(content_list)
        list_author.extend(list(set(author_list)))

    for index in range(len(list_content)):
        for author in list_author:
            if author in list_content[index]['fields']['content'].strip():
                if author:
                    list_content[index]['fields']['content'] = list_content[index]['fields']['content'][:-len(author)]
                    list_content[index]['fields']['author'] = author

    json_writen(list_content, file_name)
    if parse_off == 0:
        break
