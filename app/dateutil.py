from datetime import datetime, timedelta
from .logconfig import setup_logger


def get_oldest_tefas_api_date():
    return get_nearest_weekday(datetime.now() - timedelta(days=85))

def get_nearest_weekday(date):
    """
    Return the nearest prior weekday to the given date.
    If the date is a weekday, it returns the date itself.
    If the date is a weekend, it returns the previous Friday.
    """


    logger = setup_logger(__name__)


    # Weekday of the given date (Monday is 0 and Sunday is 6)
    weekday = date.weekday()

    # If it's Saturday (5) or Sunday (6), return the previous Friday
    if weekday == 5:  # Saturday
        logger.debug(f"Queried date ({date}) is saturday returning to friday!")
        return date - timedelta(days=1)
    elif weekday == 6:  # Sunday
        logger.debug(f"Queried date ({date}) is sunday returning to friday!'")
        return date - timedelta(days=2)
    else:  # It's already a weekday
        return date

