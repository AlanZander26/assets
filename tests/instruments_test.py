import pytest
from assets.instruments import Stock, Currency, Futures, Option
from assets.utils import ExpirationDate

# Test creation of financial instruments

def test_stock_creation():
    aapl = Stock("AAPL", price=200)
    assert aapl.name == "AAPL" 
    assert aapl.price == 200
    aapl2 = Stock("AAPL", 205)
    assert aapl2 is aapl # aapl2 should be the same object as aapl
    assert aapl.price == 205
    

def test_currency_creation():
    eur = Currency("EUR", exchange_rate=1.095)
    assert eur.name == "EUR"
    assert eur.price == 1.095


def test_futures_creation():
    oil_fut = Futures(
        underlying=Stock("CL"),
        expiration="251220",
        forward_price=85.00,
        contract_size=1000,
        price=83.50
    )
    assert oil_fut.name == "CLZ20"  
    assert oil_fut.price == 83.50
    assert oil_fut.forward_price == 85.00
    assert oil_fut.contract_size == 1000
    assert oil_fut.price_at_expiration(ST=90) == 5000 


def test_option_creation_and_expiration():
    aapl = Stock("AAPL", price=200)
    aapl_call = Option(
        underlying=aapl,
        strike=205.0,
        expiration="250620",
        option_type="C",
        price=5.25
    )
    aapl_call.expiration.fix_time(1.2) # since this test will be executed in the future, we fix the time to expiration to 1.2 yr.
    assert aapl_call.option_type == "C"
    assert aapl_call.strike == 205
    assert isinstance(aapl_call.expiration, ExpirationDate)
    assert aapl_call.expiration.T == 1.2
    assert aapl_call.price == 5.25
    assert aapl_call.expiration.is_expired() == False

    aapl_put_expired = Option(
        underlying=aapl,
        strike=205.0,
        expiration="240620", # Expiration lies in the past. i.e. the option already expired
        option_type="P"
    )
    assert aapl_put_expired.price is None
    assert aapl_put_expired.expiration.is_expired()


# Test most important methods

def test_price_at_expiration():
    # Futures
    oil_fut = Futures(
        underlying=Stock("CL"),
        expiration="251220",
        forward_price=85.00,
        contract_size=1000,
        price=83.50
    )
    assert oil_fut.price_at_expiration(ST=90) == 5000 
    assert oil_fut.price_at_expiration(ST=80) == -5000 
    # Option
    pypl = Stock("PYPL", price=70)
    pypl_call = Option(
        underlying=pypl,
        strike=75.0,
        expiration="250620",
        option_type="C",
        price=5.25
    )
    assert pypl_call.price_at_expiration(ST=80) == 500
    assert pypl_call.price_at_expiration(ST=74.99) == 0


def test_invalid_option_type():
    aapl = Stock("AAPL", price=195.32)
    with pytest.raises(ValueError):
        Option(aapl, strike=200, expiration="250620", option_type="X", price=5.25)


def test_futures_invalid_expiration():
    with pytest.raises(TypeError):
        Futures(
            underlying=Stock("CL"),
            expiration=None,  # Missing expiration should raise
            forward_price=85.00,
            contract_size=1000,
            price=83.50
        )
    with pytest.raises(ValueError):
        Futures(
            underlying=Stock("CL"),
            expiration="20250815",  # raise ValueError(f"Invalid expiration date format: '{expiration_date}'. Expected 'YYMMDD'.")
            forward_price=85.00,
            contract_size=1000,
            price=83.50
        )
