from fastapi import FastAPI, Depends, Form
from fastapi import status, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from app.database.session import SessionDep
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import *
from app.schemes import *

app = FastAPI()

app.mount('/static', StaticFiles(directory='../static'), name='static')

templates = Jinja2Templates(directory='../templates')


@app.get('/', response_class=HTMLResponse)
async def home(request: Request, session: AsyncSession = SessionDep(commit=True)):
    await UpdateDataService.update_database_matches(session)
    categories = await CategoryService.find_all(session)

    return templates.TemplateResponse(request=request, name='home.html', context={'categories': categories})


@app.get('/matches/{index}')
async def candles(request: Request, index: int, session: AsyncSession = SessionDep()):
    find_category = await CategoryService.get_category_with_matches_and_price_list(session, index)

    matches = sorted(find_category.matches, key=lambda x: x.name)

    return templates.TemplateResponse(
        request=request,
        name='list.html',
        context={
            'matches': matches,
            'category_id': find_category.id,
            'category_title': find_category.title
        }
    )


@app.get('/shopping/{category_id}')
async def shopping(request: Request, category_id: int, session: AsyncSession = SessionDep()):
    shops = await ShopService.find_all(session)

    price = 0
    for i in shops:
        price += i.match_price

    return templates.TemplateResponse(
        request=request,
        name='shopping.html',
        context={'shop_item': shops, 'all_price': price, 'url': category_id}
    )


@app.get('/more/{category_id}/{index}')
async def more(request: Request, category_id: int, index: int, session: AsyncSession = SessionDep()):
    find_match = await MatchService.get_match_with_comments(session, index)

    return templates.TemplateResponse(
        request=request,
        name='more.html',
        context={'candle': find_match, 'url': category_id}
    )


@app.post('/more/{category_id}/{index}')
async def add(index: int, category_id: int, comm=Form(), star=Form(), session: AsyncSession = SessionDep(commit=True)):
    find_match = await MatchService.get_match_with_comments(session, index)

    create_comment = CommentScheme(content=comm, star=star, match_id=find_match.id)
    await CommentService.add(session, create_comment)

    sum = 0
    for i in find_match.comments:
        sum += i.star
    if len(find_match.comments) == 0:
        find_match.star = int(sum)
    else:
        find_match.star = int(sum / len(find_match.comments))

    return RedirectResponse(f'/more/{category_id}/{index}', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/sort/{sorted_by}/{category_id}')
async def sort(request: Request, sorted_by: str, category_id: int, session: AsyncSession = SessionDep()):
    expected_url = ['sorted_by_stars', 'sorted_by_price']
    find_category = await CategoryService.get_category_with_matches_and_price_list(session, category_id)

    if sorted_by == expected_url[0]:
        matches = sorted(find_category.matches, key=lambda x: x.star)
    elif sorted_by == expected_url[1]:
        matches = sorted(find_category.matches, key=lambda x: x.expected_price)

    return templates.TemplateResponse(
        request=request,
        name='list.html',
        context={
            'matches': matches,
            'category_id': find_category.id,
            'category_title': find_category.title
        }
    )


@app.post('/shopping_add/{id_id}/{list_id}/{url}')
async def shopping_add(id_id: int, list_id: int, url: int, session: AsyncSession = SessionDep(commit=True)):
    candle = await MatchService.find(session, id_id)
    price_item = await PriceListService.find(session, list_id)

    shop_item = ShopScheme(match_name=candle.name, match_edition=price_item.edition, match_price=price_item.all_price)
    await ShopService.add(session, shop_item)

    return RedirectResponse(f'/shopping/{url}', status_code=status.HTTP_303_SEE_OTHER)


@app.post('/shopping_del/{shop_id}/{url}')
async def shoping_del(shop_id: int, url: str, session: AsyncSession = SessionDep(commit=True)):
    await ShopService.delete(session, shop_id)

    return RedirectResponse(f'/shopping/{url}', status_code=status.HTTP_303_SEE_OTHER)


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
