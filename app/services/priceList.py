from app.models import PriceList
from app.database.service import BaseService


class PriceListService(BaseService[PriceList]):
    model = PriceList
