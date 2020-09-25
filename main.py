from requests import get
from bs4 import BeautifulSoup
from warnings import warn
from time import sleep
from random import randint
import numpy as np
import pandas as pd

# initialize empty lists to store the variables scraped
names = []
sizes = []
spheres = []
okeds = []
statuses = []
company_types = []
contacts = []

iterations = 0

for page in range(1, 10000):

    # get request
    response = get(
        "http://businessnavigator.kz/ru/branch/?PAGEN_1=" + str(page) + "&SIZEN_1=20")

    # throw warning for status codes that are not 200
    if response.status_code != 200:
        warn('Request: {}; Status code:{}'.format(
            requests, response.status_code))

    # parse the content of current iteration of request
    page_html = BeautifulSoup(response.text, 'lxml')

    item_containers = page_html.find_all(
        'tr')[1:]

    for container in item_containers:

        tds = container.find_all('td')

        name = tds[0].a.text
        names.append(name)

        size = tds[1].text
        sizes.append(size)

        sphere = tds[2].text
        spheres.append(sphere)

        oked = tds[3].text
        okeds.append(oked)

        status = tds[4].text
        statuses.append(status)

        company_type = tds[5].text
        company_types.append(company_type)

        contact = tds[6].text
        contacts.append(contact)

        iterations += 1
        print("Finished iteration: " + str(iterations))


companies_df = pd.DataFrame({'Название': names,
                             'Кол-во сотрудников': sizes,
                             'Вид деятельности': spheres,
                             'ОКЭД': okeds,
                             'Статус': statuses,
                             'Форма собствености': company_types,
                             'Адрес фактический': contacts,
                             })


companies_df.to_csv("companies.csv", index=False)
