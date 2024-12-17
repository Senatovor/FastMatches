from fastapi import FastAPI, Depends, Form
from fastapi import status, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from db_classes import Comment, SafetyMatch, MatchCat, PriceList, Shop


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

db_name = 'sql_app.db'
SQLALCHEMY_DATABASE_URL = f'sqlite:///instance/{db_name}'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})


def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home(request: Request):
    return templates.TemplateResponse(request=request, name='home.html')


@app.get('/shopping/{url}')
def shopping(request: Request, url: str, db: sessionmaker = Depends(get_db)):
    array = db.query(Shop).all()

    price = 0
    for i in array:
        price += i.match_price

    return templates.TemplateResponse(request=request, name='shopping.html', context={'shop_item': array, 'all_price': price, 'url': url})


@app.get('/{url}')
def candles(request: Request, url: str, db: sessionmaker = Depends(get_db)):
    candles_catagory = db.query(MatchCat).filter(MatchCat.catagory == url).first()

    candlesing = candles_catagory.cat_id
    candlesing.sort(key=lambda candle: candle.name, reverse=True)

    if candles_catagory is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return templates.TemplateResponse(request=request, name='list.html', context={'candle': candles_catagory})


@app.get('/more/{url}/{id_id}')
def more(request: Request, id_id: int, url: str, db: sessionmaker = Depends(get_db)):
    candle = db.get(SafetyMatch, id_id)

    if candle is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return templates.TemplateResponse(request=request, name='more.html', context={'candle': candle, 'url': url})


@app.post('/more/{url}/{id_id}')
def add(id_id: int, url: str, comm=Form(), star=Form(), db: sessionmaker = Depends(get_db)):
    candle = db.get(SafetyMatch, id_id)
    if candle is None:
        raise HTTPException(status_code=404, detail="Category not found")

    commentar = Comment(comment=comm, stars=star, match_id=candle.id)
    db.add(commentar)
    db.commit()

    sum = 0
    for i in candle.commentaring:
        sum += i.stars
    candle.star = int(sum / len(candle.commentaring))
    db.commit()
    db.refresh(candle)

    return RedirectResponse(f'/more/{url}/{id_id}', status_code=status.HTTP_303_SEE_OTHER)


@app.get('/{sorted_by}/{url}')
def sort(request: Request, sorted_by: str, url: str, db: sessionmaker = Depends(get_db)):
    expexted_url = ['sorted_by_stars', 'sorted_by_price', 'sorted_by_time']
    candles_catagory = db.query(MatchCat).filter(MatchCat.catagory == url).first()

    if candles_catagory is None:
        raise HTTPException(status_code=404, detail="Category not found")

    candles = candles_catagory.cat_id

    if sorted_by == expexted_url[0]:
        candles.sort(key=lambda candle: candle.star, reverse=True)
    elif sorted_by == expexted_url[1]:
        candles.sort(key=lambda candle: candle.expected_price, reverse=True)
    elif sorted_by == expexted_url[2]:
        candles.sort(key=lambda candle: candle.time, reverse=True)

    return templates.TemplateResponse(request=request, name='list.html', context={'candle': candles_catagory})


@app.post('/shopping_add/{id_id}/{list_id}/{url}')
def shopping_add(id_id: int, list_id: int, url: str, db: sessionmaker = Depends(get_db)):
    candle = db.get(SafetyMatch, id_id)
    price_item = db.get(PriceList, list_id)

    shop_item = Shop(match_name=candle.name, match_edition=price_item.edition, match_price=price_item.all_price)
    db.add(shop_item)
    db.commit()

    return RedirectResponse(f'/shopping/{url}', status_code=status.HTTP_303_SEE_OTHER)


@app.post('/shopping_del/{shop_id}/{url}')
def shoping_del(shop_id: int, url: str, db: sessionmaker = Depends(get_db)):
    shop_item = db.get(Shop, shop_id)
    db.delete(shop_item)
    db.commit()

    return RedirectResponse(f'/shopping/{url}', status_code=status.HTTP_303_SEE_OTHER)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
