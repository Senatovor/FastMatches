from bs4 import BeautifulSoup
import requests
from db_classes import PriceList, MatchCat, SafetyMatch
import re


url_content = ['spichki-v-korobkah-2',
               'sigarnye-spichk',
               'spichki-v-flakonah',
               'spichki-knijki',
               'kaminnye-spichki',
               'specialnye-vidy-spichek']


def parsing_prices(url: str):
    tables = []
    table = []
    price_array = []
    prices_array = []

    request = requests.get(url)
    html_content = request.content
    soup = BeautifulSoup(html_content, 'html.parser')

    for data in soup.find_all('div', class_='ma-accordion-tab-content'):
        tables.append(data)

    for data in tables:
        if data.find_all('tr'):
            prices = data.find_all('tr')
            for price in prices:
                price_array.append(price.text.split())
            table.append(price_array)
            price_array = []

    for prices in table:
        price_array = []

        for price in prices[1:-1]:
            if len(price) == 1:
                number = price[0][1:].lstrip('0')
                pair = [price[0].replace(number, ''), number]
                price_array.append([int(pair[0]), float(pair[1])])
            else:
                price_array.append([int(price[0]), float(price[1])])

        prices_array.append(price_array)

    return prices_array


def parsing_math(url: str):
    tables = []
    names_and_descriptions = []

    request = requests.get(url)
    html_content = request.content
    soup = BeautifulSoup(html_content, 'html.parser')
    for data in soup.find_all('div', class_='elementor-image-box-wrapper'):
        tables.append(data)

    math = soup.find_all('h5')
    description = soup.find_all('p', class_='elementor-image-box-description')

    if len(math) == len(description):
        start = 0
    else:
        start = 1

    for i, j in zip(math, description[start:]):
        names_and_descriptions.append([i.text, j.text.replace('\n', ' ')])  # Если нужны \n -> убираем replace

    return names_and_descriptions


def parsing_img(url: str):
    tables = []
    imges = []
    request = requests.get(url)
    html_content = request.content
    soup = BeautifulSoup(html_content, 'html.parser')
    for data in soup.find_all('div', class_='elementor-image-box-wrapper'):
        tables.append(data)

    array = []
    for i in tables:
        array.append(i.find_all('img'))
    for j in array:
        if j:
            imges.append(j[0]['src'])

    return imges


def give(urls):
    array_matches_cat = []

    for url_name in urls:
        url = f'https://spichkata.ru/{url_name}/'
        prices = parsing_prices(url)
        mathes = parsing_math(url)
        imges = parsing_img(url)
        array = []
        first_digit = 0
        first_number = 0
        second_digit = 0
        for price, math, img in zip(prices, mathes, imges):
            array_price = []
            for i in price:
                array_price.append(PriceList(edition=i[0], price=i[1], all_price=round(i[0]*i[1])))

            text = math[1]

            brackets_content = re.findall(r'\((.*?)\)', text)

            if len(brackets_content) == 1:
                first_number_before_x = re.search(r'(\d+)x', brackets_content[0])
                if first_number_before_x:
                    first_number = first_number_before_x.group(1)
            else:
                brackets_content = re.findall(r'\((.*?)\)', text)
                if brackets_content:
                    last_content = brackets_content[-1]
                    number_after_last_x = re.search(r'[xх](\d+)', last_content)
                    if number_after_last_x:
                        first_number = number_after_last_x.group(1)

            match_filling = re.search(r'Наполнение\s*(\d+)', text)
            if match_filling:
                filling_number = match_filling.group(1)
                time = int(((int(first_number) * int(filling_number)) / 100 - 1) * 5)
            else:
                match = re.search(r"(\d+)х(\d+)", text)
                if match:
                    first_digit = int(match.group(1))
                    second_digit = int(match.group(2))
                time = int(((int(first_digit) * int(second_digit)) / 100 - 1) * 5)

            object_math = SafetyMatch(name=math[0], description=math[1], price_list=array_price, time=time, star=0,
                                      expected_price=array_price[0].all_price, img=img)
            array.append(object_math)

        match_cat = MatchCat(catagory=url_name, cat_id=array)

        array_matches_cat.append(match_cat)

    return array_matches_cat
