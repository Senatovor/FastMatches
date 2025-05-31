from pydantic import BaseModel, ConfigDict
from typing import List


class PriceListScheme(BaseModel):
    edition: int
    price: float
    all_price: int
    match_id: int

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
