from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from datetime import datetime, timedelta
import time

load_dotenv()


class Settings(BaseSettings):
    USERNAME: str
    PASSWORD: str
    LOGIN_PAGE: str
    RESERVATION_PAGE: str
    ACCOUNT_PAGE: str
    DAY: str
    DATE: int
    MONTH_NBR: int
    YEAR: int
    SLOT: str
    DURATION: str
    FIRST_NAME: str
    LAST_NAME: str
    GYMLIB_CODES: list
    EMAILS: list
    SECONDS_BEFORE_START: int
    CARD_NUMBER: str
    EXP_DATE: str
    CVC: str
    USER_AGENT: str


settings = Settings()


def get_cur_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


def print_log(*args: any):
    print(get_cur_time(), *args)
