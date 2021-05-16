import requests
import csv
from bs4 import BeautifulSoup


def csv_write(data: list):
    with open('content.csv', 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['title', 'alias'])
        for line in data:
            writer.writerow(line)


def parse_type_page(url: str, type_tag: str) -> list:
    """
        Функция запроса на получение всех страниц сайта
        url - это sitemap.xml
        typ_tag - html tag в котором находится ссылка на страницу
    """
    query = requests.get(url)
    soup = BeautifulSoup(query.text, 'html.parser')
    result = soup.find_all(type_tag)
    return result


def list_link(array: list) -> list:
    """
        Функция изменения массива
    """
    list_links = []
    for link in array:
        list_links.append(link.text)
    return list_links


def query_link_page(array: list) -> list:
    """
        Функция запроса к определенной странице из массива
        и получение ее название, контента и ссылки
    """
    result = []
    for item in array:
        try:
            query = requests.get(item)
            soup = BeautifulSoup(query.text, 'html.parser')
            title_page = soup.find('meta', {'name': 'h1'})
            alias_page = soup.find('meta', {'name': 'alias'})
            result.append({
                'title': title_page.get('content'),
                'alias': alias_page.get('content')
            })
        except AttributeError:
            print(item, AttributeError)
    return result


res_query = parse_type_page('https://angel-loves.com/sitemap.xml', 'loc')
res_link = list_link(res_query)
res_query_page = query_link_page(res_link)
csv_write(res_query_page)
