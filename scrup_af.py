import requests
import csv
from bs4 import BeautifulSoup


URL = 'https://angel-loves.com/aforizmy/aforizmy-pro-revnost.html'


def csv_write(data: list):
    with open('data.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['title', 'author'])
        for line in data:
            writer.writerow(line)
    csv_file.close()


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
            'title': text,
            'author': new_author
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
csv_write(all_resource)
