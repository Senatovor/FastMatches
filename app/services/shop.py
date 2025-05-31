from app.models import Shop
from app.database.service import BaseService


class ShopService(BaseService[Shop]):
    model = Shop