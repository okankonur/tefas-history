from .fetch import fetch_data
from datetime import datetime
from .database import TefasDatabase
from .email import send_email

def main():

    database = TefasDatabase()

    database.update_and_save_profit_ratios()

    df = fetch_data()
    database.update_main_tefas_table(df)

    send_email("profit_output.xlsx")

if __name__ == "__main__":
    main()
