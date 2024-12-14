from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    app_title: str = 'Сервис управления пользователями и транзакциями (0.1)'
    description: str = ('Система, позволяющая пользователям регистрироваться,'
                        'аутентифицироваться и осуществлять переводы средств с учетом безопасности и удобства.')
    database_url: str = 'sqlite+aiosqlite:///./user_transaction.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        env_file = '.env'


settings = Settings()
