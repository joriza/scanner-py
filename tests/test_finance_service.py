"""
Tests unitarios para FinanceService.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

from finance_service import FinanceService
from database import Ticker, Price


class TestFinanceService:
    """Tests para la clase FinanceService."""
    
    def test_normalize_symbol_basic(self):
        """Test normalización básica de símbolos."""
        assert FinanceService.normalize_symbol('AAPL') == 'AAPL'
        assert FinanceService.normalize_symbol('TSLA') == 'TSLA'
    
    def test_normalize_symbol_ba(self):
        """Test normalización de símbolos BCBA."""
        assert FinanceService.normalize_symbol('BCBA:AAPL') == 'AAPL.BA'
        assert FinanceService.normalize_symbol('BCBA:GGAL') == 'GGAL.BA'
    
    def test_normalize_symbol_with_dot(self):
        """Test normalización de símbolos con punto."""
        assert FinanceService.normalize_symbol('BRK.B') == 'BRK-K'
        assert FinanceService.normalize_symbol('BF.B') == 'BF-K'
    
    def test_normalize_symbol_whitespace(self):
        """Test normalización de símbolos con espacios."""
        assert FinanceService.normalize_symbol('  AAPL  ') == 'AAPL'
        assert FinanceService.normalize_symbol(' TSLA ') == 'TSLA'
    
    @patch('yfinance.download')
    def test_sync_ticker_data_success(self, mock_download, db_session, sample_ticker):
        """Test sincronización exitosa de ticker."""
        # Configurar mock
        dates = pd.date_range('2024-01-01', periods=10, freq='D')
        mock_data = pd.DataFrame({
            'Open': [100.0] * 10,
            'High': [105.0] * 10,
            'Low': [95.0] * 10,
            'Close': [102.0] * 10,
            'Volume': [1000000] * 10
        }, index=dates)
        mock_download.return_value = mock_data
        
        # Ejecutar sincronización
        count = FinanceService.sync_ticker_data(sample_ticker)
        
        # Verificar
        assert count == 10
        assert mock_download.called
        assert sample_ticker.last_sync is not None
    
    @patch('yfinance.download')
    def test_sync_ticker_data_with_duplicates(self, mock_download, db_session, sample_ticker):
        """Test sincronización con datos duplicados."""
        # Configurar mock
        dates = pd.date_range('2024-01-01', periods=10, freq='D')
        mock_data = pd.DataFrame({
            'Open': [100.0] * 10,
            'High': [105.0] * 10,
            'Low': [95.0] * 10,
            'Close': [102.0] * 10,
            'Volume': [1000000] * 10
        }, index=dates)
        mock_download.return_value = mock_data
        
        # Primera sincronización
        count1 = FinanceService.sync_ticker_data(sample_ticker)
        assert count1 == 10
        
        # Segunda sincronización (no debería agregar duplicados)
        count2 = FinanceService.sync_ticker_data(sample_ticker)
        assert count2 == 0
    
    @patch('yfinance.download')
    def test_sync_ticker_data_empty_response(self, mock_download, db_session, sample_ticker):
        """Test sincronización con respuesta vacía."""
        # Configurar mock para retornar DataFrame vacío
        mock_download.return_value = pd.DataFrame()
        
        # Ejecutar sincronización
        count = FinanceService.sync_ticker_data(sample_ticker)
        
        # Verificar
        assert count == 0
    
    @patch('yfinance.download')
    def test_sync_ticker_data_with_multiindex(self, mock_download, db_session, sample_ticker):
        """Test sincronización con MultiIndex en columnas."""
        # Configurar mock con MultiIndex
        dates = pd.date_range('2024-01-01', periods=5, freq='D')
        arrays = [['Open', 'High', 'Low', 'Close', 'Volume'], ['Adj Close']]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples)
        
        mock_data = pd.DataFrame(
            [[100.0, 102.0, 98.0, 101.0, 1000000, 101.0]] * 5,
            index=dates,
            columns=index
        )
        mock_download.return_value = mock_data
        
        # Ejecutar sincronización
        count = FinanceService.sync_ticker_data(sample_ticker)
        
        # Verificar que se maneje correctamente
        assert count == 5
    
    def test_get_signals_rsi_macd(self, db_session, sample_ticker, sample_prices):
        """Test cálculo de señales RSI + MACD."""
        signals = FinanceService.get_signals(sample_ticker, strategy='rsi_macd')
        
        # Verificar estructura
        assert signals is not None
        assert 'symbol' in signals
        assert 'price' in signals
        assert 'rsi' in signals
        assert 'macd_status' in signals
        assert signals['symbol'] == 'AAPL'
    
    def test_get_signals_3_emas(self, db_session, sample_ticker, sample_prices):
        """Test cálculo de señales 3 EMAs."""
        signals = FinanceService.get_signals(sample_ticker, strategy='3_emas')
        
        # Verificar estructura
        assert signals is not None
        assert 'symbol' in signals
        assert 'emas_d_active' in signals
        assert 'emas_w_active' in signals
        assert 'ema4_d' in signals
        assert 'ema9_d' in signals
        assert 'ema18_d' in signals
    
    def test_get_signals_insufficient_data(self, db_session, sample_ticker):
        """Test cálculo de señales con datos insuficientes."""
        # Agregar solo 20 precios (menos que el mínimo de 30)
        base_date = datetime(2024, 1, 1)
        for i in range(20):
            price = Price(
                ticker_id=sample_ticker.id,
                date=base_date + timedelta(days=i),
                open=100.0 + i,
                high=105.0 + i,
                low=95.0 + i,
                close=102.0 + i,
                volume=1000000
            )
            db_session.add(price)
        db_session.commit()
        
        # Verificar que retorne None
        signals = FinanceService.get_signals(sample_ticker, strategy='rsi_macd')
        assert signals is None
    
    def test_get_signals_invalid_strategy(self, db_session, sample_ticker, sample_prices):
        """Test cálculo de señales con estrategia inválida."""
        # Debería manejar estrategias inválidas graciosamente
        signals = FinanceService.get_signals(sample_ticker, strategy='invalid_strategy')
        # Si no maneja la estrategia, debería retornar None o el resultado por defecto
        assert signals is None or 'symbol' in signals


class TestFinanceServiceIntegration:
    """Tests de integración para FinanceService."""
    
    @patch('yfinance.download')
    def test_full_sync_workflow(self, mock_download, db_session):
        """Test flujo completo de sincronización."""
        # Crear ticker
        ticker = Ticker(symbol='TEST', is_active=True)
        db_session.add(ticker)
        db_session.commit()
        
        # Configurar mock
        dates = pd.date_range('2024-01-01', periods=30, freq='D')
        mock_data = pd.DataFrame({
            'Open': [100.0 + i for i in range(30)],
            'High': [105.0 + i for i in range(30)],
            'Low': [95.0 + i for i in range(30)],
            'Close': [102.0 + i for i in range(30)],
            'Volume': [1000000 + i * 10000 for i in range(30)]
        }, index=dates)
        mock_download.return_value = mock_data
        
        # Sincronizar
        count = FinanceService.sync_ticker_data(ticker)
        
        # Verificar
        assert count == 30
        assert ticker.last_sync is not None
        
        # Calcular señales
        signals = FinanceService.get_signals(ticker, strategy='rsi_macd')
        
        # Verificar que se calcularon señales
        assert signals is not None
        assert 'rsi' in signals
        assert signals['rsi'] is not None
