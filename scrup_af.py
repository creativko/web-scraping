import requests
import json
from bs4 import BeautifulSoup


URL = 'https://angel-loves.com/aforizmy/aforizmy-pro-revnost.html'
MODEL = 'aphorisms.Aphorisms'
PK = 1
CAT_ID = 1


def json_writen(data):
    with open('data.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file)


def query_paginate(link: str):
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    page_list = soup.find_all('span', {'class': 'pagelist'})
    link_list = f'{link}?page='
    result = [link_list + item.get_text() for item in page_list]
    return result


def query_page(link: str):
    """Данные с одной страницы"""
    query = requests.get(link)
    soup = BeautifulSoup(query.text, 'html.parser')
    result = soup.find_all('div', {'class': 'center_live'})
    result_author = soup.select("div.center_live span")
    count = len(result_author)
    response = []
    counter = 0
    for item in result:
        new_author = str(result_author[counter].get_text())
        new_str = str(item.get_text())
        new_str = new_str.strip()
        text = new_str[:-len(new_author)]
        response.append({
            'model': MODEL,
            'pk': PK,
            'fields': {
                'content': text,
                'author': new_author,
                'category': CAT_ID,
            }
        })
        if counter > count:
            break
        counter += 1
    return response


pages = query_paginate(URL)
all_resource = []
for page in pages:
    q = query_page(page)
    all_resource.extend(q)
json_writen(all_resource)
