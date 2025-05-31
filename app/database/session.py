from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from app.config import settings
from functools import wraps
from fastapi import Depends

SQL_DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=SQL_DATABASE_URL)
session_factory = async_sessionmaker(engine, expire_on_commit=False)


class DatabaseSessionManager:
    """Класс для работы с сессиями"""

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]):
        self.session_factory = session_maker

    def session_dependency(self, isolation_level: str | None = None, commit: bool = False):
        """
        Зависимость для FastAPI. Создает сессию, самостоятельно её закрывает, делает rollback при ошибке.
        Имеет настройку авто-commit и уровня изоляции.
        """
        async def get_session():
            async with self.session_factory() as session:
                try:
                    if isolation_level:
                        await session.execute(
                            text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}")
                        )
                    yield session
                    if commit:
                        await session.commit()
                except Exception:
                    await session.rollback()
                    raise
                finally:
                    await session.close()

        return Depends(get_session)

    def connection(self, isolation_level: str | None = None, commit: bool = False):
        """
        Декоратор. Создает сессию, самостоятельно её закрывает, делает rollback при ошибке.
        Имеет настройку авто-commit и уровня изоляции.
        """
        def decorator(method):
            @wraps(method)
            async def wrapper(*args, **kwargs):
                async with self.session_factory() as session:
                    try:
                        if isolation_level:
                            await session.execute(text(f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"))
                        result = await method(*args, session=session, **kwargs)
                        if commit:
                            await session.commit()
                        return result
                    except Exception:
                        await session.rollback()
                        raise
                    finally:
                        await session.close()

            return wrapper

        return decorator


session_manager = DatabaseSessionManager(session_factory)
SessionDep = session_manager.session_dependency


# Пример использования зависимости для FastAPI
#
# @app.get("/")
# async def test(session: AsyncSession = SessionDep(commit=True)):
#     session.add(User(name='Пеня', gender='MALE'))
#     return {"message": "User created"}
