import requests
from bs4 import BeautifulSoup
import csv
import time
import lxml

start_time = time.time()
with open('res.csv', 'w', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow([
        'Наименование', 'Описание', 'Цена'])

url = 'https://catalog.onliner.by/sdapi/catalog.api/search/videocard?page=2'
session = requests.Session()
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

}

req = session.get(url=url, headers=headers).json()

c = 0
result_csv = []
for n, i in enumerate( req['products'], 1):
    print(f'{n}: {i["html_url"]}')
    item_url = i['html_url']
    response_item = session.get(url=item_url, headers=headers)
    response_item.encoding = 'utf-8'
    soup = BeautifulSoup(response_item.text, 'lxml')
    name = soup.find('h1', class_='catalog-masthead__title js-nav-header')
    disk = soup.find('div', class_='offers-description__specs')
    price = soup.find('a', class_='offers-description__link offers-description__link_nodecor js-description-price-link')
    result_csv.append([name.text.strip(), disk.text.strip(), price.text.strip()])


with open('res.csv', 'a', encoding='utf-8-sig', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    for item, descr, price in result_csv:

        # Формируем строку для записи
        flatten = item,descr, price
        writer.writerow(flatten)
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Время работы программы = {elapsed_time}')
print('Файл res.csv создан')

#Время работы программы = 42.84527015686035
#Время работы программы = 46.16775465011597 с сессией в титле
#Время работы программы = 34.22930359840393 с сессией а титле и итем