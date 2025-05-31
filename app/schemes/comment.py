from pydantic import BaseModel, ConfigDict


class CommentScheme(BaseModel):
    content: str
    star: int
    match_id: int

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
