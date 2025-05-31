from pydantic import BaseModel, ConfigDict, Field


class ShopScheme(BaseModel):
    match_name: str
    match_edition: int
    match_price: int

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)