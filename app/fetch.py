from tefas import Crawler
from datetime import datetime, timedelta
from .database import SessionLocal, desc
from .models import TefasModel
import logging

def get_date_three_months_ago():
    """
    Returns the date which is three months prior to the current date.
    The date is returned in the format 'YYYY-MM-DD'.
    """
    # Current date
    current_date = datetime.now()

    # Calculate the date three months ago
    # For simplicity, we consider 3 months as approximately 90 days
    months_ago_date = current_date - timedelta(days=90)

    # Format the date in 'YYYY-MM-DD' format
    return months_ago_date.strftime('%Y-%m-%d')

def get_formatted_current_date():
    current_date_time = datetime.now()
    formatted_date = current_date_time.strftime("%Y-%m-%d")
    return formatted_date


def fetch_data():

    tefas_crawler = Crawler()

    db = SessionLocal()
    latest_date = db.query(TefasModel.date).order_by(desc(TefasModel.date)).first()
    if latest_date:
        latest_date_str = latest_date[0].strftime('%Y-%m-%d')
        logging.info(f"The latest date in the database is: {latest_date_str}")
    else:
        logging.warn("No dates found in the table.")

    return tefas_crawler.fetch(start=latest_date_str, end=get_formatted_current_date())


