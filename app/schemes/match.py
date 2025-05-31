from pydantic import BaseModel, ConfigDict, Field


class MatchScheme(BaseModel):
    name: str
    description: str
    star: int
    expected_price: int
    img: str
    category_id: int

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
