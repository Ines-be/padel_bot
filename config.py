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
    CARD_NUMBER: str
    EXP_DATE: str
    CVC: str


settings = Settings()


def start_bot():
    """Wait until 2 seconds before the slot is available to start"""
    slot_time = settings.SLOT.split(":")
    target_time = datetime(
        settings.YEAR,
        settings.MONTH_NBR,
        int(settings.DATE),
        int(slot_time[0]),
        int(slot_time[1]),
        0,
    )
    start_time = target_time - timedelta(days=6, seconds=2)

    print("Target slot = ", target_time, settings.DURATION)
    print("Start time = ", start_time)

    print("Waiting...")
    while datetime.now() < start_time:
        time.sleep(0.5)
    print("Starting")
