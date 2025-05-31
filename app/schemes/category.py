from pydantic import BaseModel, ConfigDict
from typing import List


class CategoryScheme(BaseModel):
    title: str
    url: str

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
