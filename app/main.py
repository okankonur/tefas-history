from .fetch import fetch_data
from datetime import datetime
from .database import TefasDatabase
from .email import send_email

def main():

    database = TefasDatabase()

    df = fetch_data()
    database.update_main_tefas_table(df)

    database.update_and_save_profit_ratios()

    send_email("profit_output.xlsx")

if __name__ == "__main__":
    main()
