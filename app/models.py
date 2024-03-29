from sqlalchemy import Column, Integer, Float, String, Date, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TefasModel(Base):
    __tablename__ = 'tbl_tefas'
    id = Column(Integer, primary_key=True)
    price = Column(Float)
    title = Column(String)
    market_cap = Column(Float)
    number_of_shares = Column(Float)
    number_of_investors = Column(Integer)
    date = Column(Date)
    tmm = Column(Float)
    repo = Column(Float)
    code = Column(String)
    other = Column(Float)
    stock = Column(Float)
    eurobonds = Column(Float)
    bank_bills = Column(Float)
    derivatives = Column(Float)
    reverse_repo = Column(Float)
    term_deposit = Column(Float)
    treasury_bill = Column(Float)
    foreign_equity = Column(Float)
    government_bond = Column(Float)
    precious_metals = Column(Float)
    commercial_paper = Column(Float)
    fx_payable_bills = Column(Float)
    foreign_securities = Column(Float)
    private_sector_bond = Column(Float)
    participation_account = Column(Float)
    foreign_currency_bills = Column(Float)
    asset_backed_securities = Column(Float)
    real_estate_certificate = Column(Float)
    foreign_debt_instruments = Column(Float)
    government_lease_certificates = Column(Float)
    fund_participation_certificate = Column(Float)
    government_bonds_and_bills_fx = Column(Float)
    private_sector_lease_certificates = Column(Float)
    # Composite Unique Constraint
    __table_args__ = (UniqueConstraint('date', 'code', name='_date_code_uc'),)


class TefasProfitModel(Base):
    __tablename__ = 'tbl_tefas_profit'
    id = Column(Integer, primary_key=True)
    code = Column(String)
    date = Column(Date)
    profit_1_month = Column(Float)
    profit_3_months = Column(Float)
    profit_6_months = Column(Float)
    profit_1_year = Column(Float)