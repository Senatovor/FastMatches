from sqlalchemy.ext.asyncio import AsyncSession
from app.utils import *
from app.schemes import *
from app.services.match import MatchService
from app.services.priceList import PriceListService
from app.services.category import CategoryService
from app.utils.parser import parsing_сategories_name_and_href, get_soup, parsing_img, parsing_math


class UpdateDataService:
    @staticmethod
    async def update_database_matches(session: AsyncSession):
        urls = parsing_сategories_name_and_href(get_soup('https://spichkata.ru/produkcija/'))

        for title, url_name in urls.items():
            url = f'https://spichkata.ru/{url_name}/'
            soup = get_soup(url)
            prices = parsing_prices(soup)
            matches = parsing_math(soup)
            images = parsing_img(soup)
            for price, math, img in zip(prices, matches, images):

                category_scheme = CategoryScheme(title=title, url=url_name)
                find_category = await CategoryService.find_one_by(session, category_scheme)
                if find_category is None:
                    find_category = await CategoryService.add(session, category_scheme)

                match_scheme = MatchScheme(
                    name=math[0],
                    description=math[1],
                    star=0,
                    expected_price=round(price[0][0] * price[0][1]),
                    img=img,
                    category_id=find_category.id
                )
                find_match = await MatchService.find_one_by(session, match_scheme)
                if find_match is None:
                    find_match = await MatchService.add(session, match_scheme)

                for i in price:
                    price_list_scheme = PriceListScheme(
                        edition=i[0],
                        price=i[1],
                        all_price=round(i[0] * i[1]),
                        match_id=find_match.id
                    )
                    find_price_list = await PriceListService.find_one_by(session, price_list_scheme)
                    if find_price_list is None:
                        await PriceListService.add(session, price_list_scheme)
