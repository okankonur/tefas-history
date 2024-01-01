from .fetch import fetch_data
from .database import SessionLocal, init_db
from .models import TefasModel
from datetime import datetime
import logging
import time

def main():
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ])

    init_db()

    fetch_start_time = time.time()
    df = fetch_data() 
    fetch_end_time = time.time()

    logging.info(f"fetch took {fetch_end_time - fetch_start_time} seconds")
    logging.info("database loop statrting...")


    db_start_time = time.time()
    
    for index, row in df.iterrows():
        try:
            db = SessionLocal()
            db_obj = TefasModel(
                price=row['price'],
                title=row['title'],
                market_cap=row['market_cap'],
                number_of_shares=row['number_of_shares'],
                number_of_investors=row['number_of_investors'],
                date=row['date'], 
                tmm=row['tmm'],
                repo=row['repo'],
                code=row['code'],
                other=row['other'],
                stock=row['stock'],
                eurobonds=row['eurobonds'],
                bank_bills=row['bank_bills'],
                derivatives=row['derivatives'],
                reverse_repo=row['reverse_repo'],
                term_deposit=row['term_deposit'],
                treasury_bill=row['treasury_bill'],
                foreign_equity=row['foreign_equity'],
                government_bond=row['government_bond'],
                precious_metals=row['precious_metals'],
                commercial_paper=row['commercial_paper'],
                fx_payable_bills=row['fx_payable_bills'],
                foreign_securities=row['foreign_securities'],
                private_sector_bond=row['private_sector_bond'],
                participation_account=row['participation_account'],
                foreign_currency_bills=row['foreign_currency_bills'],
                asset_backed_securities=row['asset_backed_securities'],
                real_estate_certificate=row['real_estate_certificate'],
                foreign_debt_instruments=row['foreign_debt_instruments'],
                government_lease_certificates=row['government_lease_certificates'],
                fund_participation_certificate=row['fund_participation_certificate'],
                government_bonds_and_bills_fx=row['government_bonds_and_bills_fx'],
                private_sector_lease_certificates=row['private_sector_lease_certificates']
            )

            logging.info(f"Saving row to db... date: {row['date']}, code: {row['code']}")
            db.add(db_obj)
            db.commit()
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                logging.warning(f"Row {index} with date {row['date']} and code {row['code']} already exists. Skipping.")
            else:
                logging.error(f"An error occurred with row {index}: {e}")
            db.rollback()
        finally:
            db.close()

    logging.info("--------COMPLETED------------")
    db_end_time = time.time()

    logging.info(f"db save took {db_end_time - db_start_time} seconds")

if __name__ == "__main__":
    main()
