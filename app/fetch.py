from tefas import Crawler
from datetime import datetime, timedelta
from .database import TefasDatabase, desc
from .logconfig import setup_logger

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

    logger = setup_logger(__name__)

    tefas_crawler = Crawler()

    database = TefasDatabase()

    latest_date_str = database.get_latest_date_in_db()
    
    return tefas_crawler.fetch(start=latest_date_str, end=get_formatted_current_date())


