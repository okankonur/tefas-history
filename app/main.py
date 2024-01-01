from .fetch import fetch_data
from .database import SessionLocal, init_db
from .models import TefasModel
from datetime import datetime

def main():
    
    init_db()

    df = fetch_data() 

    db = SessionLocal()
    try:
        for index, row in df.iterrows():
            # Create a new database object
            db_obj = TefasModel(
                price=row['price'],
                title=row['title'],
                market_cap=row['market_cap'],
                number_of_shares=row['number_of_shares'],
                number_of_investors=row['number_of_investors'],
                date=datetime.strptime(row['date'], '%Y-%m-%d'), 
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
            db.add(db_obj)
        db.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
