from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from parser import parsing_prices, parsing_math
import re
import os
from db_classes import Base, PriceList, SafetyMatch, MatchCat


db_name = 'sql_app.db'
SQLALCHEMY_DATABASE_URL = f'sqlite:///instance/{db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

url_content = ['spichki-v-korobkah-2',
               'sigarnye-spichk',
               'spichki-v-flakonah',
               'spichki-knijki',
               'kaminnye-spichki',
               'specialnye-vidy-spichek']

if not os.path.isfile("instance/sql_app.db"):
    Base.metadata.create_all(bind=engine)
    for url_name in url_content:
        url = f'https://spichkata.ru/{url_name}/'
        prices = parsing_prices(url)
        mathes = parsing_math(url)
        array = []
        for price, math in zip(prices, mathes):
            array_price = []
            for i in price:
                array_price.append(PriceList(edition=i[0], price=i[1], all_price=round(i[0]*i[1])))

            text = math[1]
            time = 0

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
                match = re.search(r"(\d+)х(\d+)", text)  # Используем re.search для поиска в любом месте строки
                if match:
                    first_digit = int(match.group(1))
                    second_digit = int(match.group(2))
                time = int(((int(first_digit) * int(second_digit)) / 100 - 1) * 5)

            object_math = SafetyMatch(name=math[0], description=math[1], price_list=array_price, time=time, star=0, expected_price=array_price[0].all_price)
            array.append(object_math)

        match_cat = MatchCat(catagory=url_name, cat_id=array)
        db.add(match_cat)
        db.commit()
