import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv


url = 'https://www.tripadvisor.ru/Restaurants-g298507-St_Petersburg_Northwestern_District.html'
tripadvisor_link = 'https://www.tripadvisor.ru'

fieldnames = ['Name', 'Mark', 'Price', 'Kitchen', 'Specialized menu', 'Adress']

page_number=0
while(True):
    page_number+=1
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    restaurants = soup.select('._15_ydu6b')

    name = []
    mark = []
    price = []
    kitchen = []
    specialized_menu = []
    adress = []

    for i in range(len(restaurants)):
        restaurants[i] = restaurants[i].get('href')
        restaurants[i] = tripadvisor_link + restaurants[i]
        new_page = requests.get(restaurants[i])
        new_soup = BeautifulSoup(new_page.text, 'html.parser')
        name.append(new_soup.select('._3a1XQ88S')[0].get_text()
        mark.append(new_soup.select('.r2Cf69qf')[0].get_text()[:3])
        price.append(new_soup.select('._1XLfiSsv')[0].get_text().replace('\xa0', ' '))
        kitchen.append(new_soup.select('._1XLfiSsv')[1].get_text())
        specialized_menu.append(new_soup.select('._1XLfiSsv')[2].get_text())
        adress.append(new_soup.select('._2saB_OSe')[0].get_text())

    frame = pd.DataFrame([name, mark, price, kitchen, specialized_menu, adress])
    frame = frame.T
    frame.columns = fieldnames
    if page_number == 1:
        frame.to_csv('all_data.csv', mode='a', index=False, sep=';')
    else:
        frame.to_csv('all_data.csv', mode='a', index=False, sep=';', header=False)

    div = soup.find('div', id='EATERY_LIST_CONTENTS')
    a_tags = div.find_all('a')
    flag = False
    for a in a_tags:
        if a.text.find('Далее') != -1:
            if (a['href']):
                url = tripadvisor_link + a['href']
                flag = True
            break
    if flag == False:
        break