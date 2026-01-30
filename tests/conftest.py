"""
Configuración de fixtures y mocks para pytest.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from app import app, db
from database import Ticker, Price


@pytest.fixture
def app_client():
    """
    Fixture que proporciona un cliente de prueba Flask.
    
    Yields:
        Flask test client
    """
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def app_context():
    """
    Fixture que proporciona el contexto de aplicación.
    
    Yields:
        Flask app context
    """
    with app.app_context():
        yield


@pytest.fixture
def db_session(app_context):
    """
    Fixture que proporciona una sesión de base de datos.
    
    Yields:
        SQLAlchemy session
    """
    session = db.session
    yield session
    session.rollback()
    session.remove()


@pytest.fixture
def mock_yfinance_download():
    """
    Fixture que mockea la función yfinance.download.
    
    Yields:
        Mock object para yfinance.download
    """
    def _mock_download(symbol, period=None, progress=False, timeout=30):
        # Retornar datos de prueba simulados
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        return pd.DataFrame({
            'Open': [100.0 + i * 0.5 for i in range(100)],
            'High': [105.0 + i * 0.5 for i in range(100)],
            'Low': [95.0 + i * 0.5 for i in range(100)],
            'Close': [102.0 + i * 0.5 for i in range(100)],
            'Volume': [1000000 + i * 10000 for i in range(100)]
        }, index=dates)
    
    with patch('yfinance.download', side_effect=_mock_download) as mock:
        yield mock


@pytest.fixture
def sample_ticker(db_session):
    """
    Fixture que crea un ticker de prueba.
    
    Args:
        db_session: Sesión de base de datos
        
    Yields:
        Ticker de prueba
    """
    ticker = Ticker(
        symbol='AAPL',
        name='Apple Inc',
        sector='Technology',
        is_active=True
    )
    db_session.add(ticker)
    db_session.commit()
    return ticker


@pytest.fixture
def sample_prices(db_session, sample_ticker):
    """
    Fixture que crea precios de prueba.
    
    Args:
        db_session: Sesión de base de datos
        sample_ticker: Ticker de prueba
        
    Yields:
        Lista de precios de prueba
    """
    prices = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(50):
        price = Price(
            ticker_id=sample_ticker.id,
            date=base_date + timedelta(days=i),
            open=100.0 + i,
            high=105.0 + i,
            low=95.0 + i,
            close=102.0 + i,
            volume=1000000
        )
        prices.append(price)
        db_session.add(price)
    
    db_session.commit()
    return prices


@pytest.fixture
def auth_headers():
    """
    Fixture que proporciona headers de autenticación (para uso futuro).
    
    Yields:
        Diccionario con headers de autenticación
    """
    return {
        'Authorization': 'Bearer test-token',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_ticker_data():
    """
    Fixture que proporciona datos de ticker de prueba.
    
    Yields:
        Diccionario con datos de ticker
    """
    return {
        'symbol': 'TSLA',
        'name': 'Tesla Inc',
        'sector': 'Technology',
        'is_active': True
    }
