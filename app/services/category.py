from app.models import Category
from app.models import Match
from app.database.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError


class CategoryService(BaseService[Category]):
    model = Category

    @classmethod
    async def get_category_with_matches_and_price_list(cls, session: AsyncSession, index: int):
        try:
            query = (
                select(cls.model)
                .options(
                    selectinload(cls.model.matches).selectinload(Match.price_list)
                )
                .filter_by(id=index)
            )
            find_category = await session.execute(query)
            return find_category.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise e
