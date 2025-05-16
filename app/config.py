import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env')
    )

    def get_db_url(self) -> str:
        return (f'postgresql+asyncpg://{settings.db_user}:{settings.db_password}@'
                f'{settings.db_host}:{settings.db_port}/{settings.db_name}')


settings = Settings()
