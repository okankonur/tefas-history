from .fetch import fetch_data
from .logconfig import setup_logger
from datetime import datetime
from .database import TefasDatabase


def main():
    
    logger = setup_logger(__name__)
    
    database = TefasDatabase()

    database.update_and_save_profit_ratios()

    df = fetch_data()
    database.update_main_tefas_table(df)

if __name__ == "__main__":
    main()
