from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from .models import Base, TefasModel, TefasProfitModel
from .logconfig import setup_logger
from .dateutil import get_nearest_weekday
from datetime import datetime, timedelta
import time



class TefasDatabase:

    DATABASE_URL = "sqlite:///./tefas.db"

    engine = create_engine(DATABASE_URL, pool_size=30, max_overflow=-1)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def __init__(self):
        self.logger = setup_logger(__name__)
        Base.metadata.create_all(bind=self.engine)
        self.logger = setup_logger(__name__)

    def calculate_profit_ratio(self, fund_code, current_date, interval):
        """
        Calculate the profit ratio for a given fund and time interval using database queries.

        :param fund_code: The fund code.
        :param current_date: The current date to calculate the profit ratio for.
        :param interval: Time interval in days.
        :return: Profit ratio as a percentage.
        """

        self.logger.info(f"Calculating profit ratio for {fund_code} on the date {current_date} for {interval} days...")
        current_price_query = self.get_fund_price_at_date(fund_code, get_nearest_weekday(current_date))
        past_date = current_date - timedelta(days=interval)
        past_price_query = self.get_fund_price_at_date(fund_code, get_nearest_weekday(past_date))

        self.logger.info(f"current price query: {current_price_query}")
        self.logger.info(f"past price query: {past_price_query}")

        if current_price_query and past_price_query:
            current_price, past_price = current_price_query[0], past_price_query[0]
            profit = ((current_price - past_price) / past_price) * 100
            self.logger.info(f"Profit for {fund_code} in {interval} days is {profit}")
            return profit
        else:
            return 0.0

    def get_fund_price_at_date(self, fund_code, date):
       date_str = date.strftime('%Y-%m-%d')
       self.logger.info(f"Querying db for {fund_code} price at {date_str}")
       with self.SessionLocal() as session:
        return self.SessionLocal().query(TefasModel.price).filter(TefasModel.code == fund_code, TefasModel.date == date_str).first()


    def get_latest_date_in_db(self):
        latest_date = self.SessionLocal().query(TefasModel.date).order_by(desc(TefasModel.date)).first()

        if latest_date:
            latest_date_str = latest_date[0].strftime('%Y-%m-%d')
            self.logger.info(f"The latest date in the database is: {latest_date_str}")
        else:
            self.logger.warn("No dates found in the table.")

        return latest_date_str

    def update_and_save_profit_ratios(self):

        self.logger.info("Starting profit ratio update...")

        current_date = datetime.now()

        with self.SessionLocal() as session:
            unique_fund_codes = session.query(TefasModel.code).distinct().all()
            unique_fund_codes = [code[0] for code in unique_fund_codes]

            self.logger.info(f"Found unique fund codes: {unique_fund_codes}")
    
            for fund_code in unique_fund_codes:
                try:
                    profit_ratio = TefasProfitModel(
                        code=fund_code,
                        date=current_date,
                        profit_1_month= self.calculate_profit_ratio(fund_code, current_date, 30),
                        profit_3_months= self.calculate_profit_ratio(fund_code, current_date, 91),
                        profit_6_months= self. calculate_profit_ratio(fund_code, current_date, 182),
                        profit_1_year= self.calculate_profit_ratio(fund_code, current_date, 365)
                     )
                    session.add(profit_ratio)
                except Exception as ex:
                    self.logger.error(f"Exception: {ex}")
                    session.rollback()
                finally:
                    self.logger.info(f"Profit ratio process completed for {fund_code}! Commiting to database!")
                    session.commit()  
                

    def update_main_tefas_table(self, df):
        self.logger.info("Starting main table update...")

        fetch_start_time = time.time() 
        fetch_end_time = time.time()
        self.logger.info(f"fetch took {fetch_end_time - fetch_start_time} seconds")
        self.logger.info(f"tefas dataframe has {len(df)} rows.")
    
        if df.empty:
            self.logger.info("Tefas dataframe is empty. No further action taken.")
            return

        self.logger.info("database loop starting...")
        db_start_time = time.time()

        with self.SessionLocal() as session:
            for index, row in df.iterrows():
                try:
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

                    self.logger.info(f"Saving row to database.SessionLocal()... date: {row['date']}, code: {row['code']}")
                    session.add(db_obj)
                    session.commit()
                except Exception as e:
                    if 'unique constraint' in str(e).lower():
                        self.logger.warning(f"Row {index} with date {row['date']} and code {row['code']} already exists. Skipping.")
                    else:
                        self.logger.error(f"An error occurred with row {index}: {e}")
                    session.rollback()
                    
            self.logger.info("--------COMPLETED------------")
            db_end_time = time.time()
            self.logger.info(f"db save took {db_end_time - db_start_time} seconds")