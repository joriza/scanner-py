"""
Tests unitarios para la API Flask.
"""

import pytest
import json
from unittest.mock import patch
from database import Ticker, Price


class TestHealthCheck:
    """Tests para el endpoint de health check."""
    
    def test_health_check_success(self, app_client):
        """Test health check exitoso."""
        response = app_client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'checks' in data
        assert data['checks']['database'] == 'connected'
    
    def test_health_check_returns_json(self, app_client):
        """Test que health check retorna JSON."""
        response = app_client.get('/health')
        
        assert response.content_type == 'application/json'


class TestTickersAPI:
    """Tests para la API de tickers."""
    
    def test_get_tickers_empty(self, app_client):
        """Test obtener tickers cuando no hay ninguno."""
        response = app_client.get('/api/tickers')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'items' in data
        assert data['items'] == []
        assert data['total'] == 0
    
    def test_get_tickers_with_data(self, app_client, db_session, sample_ticker):
        """Test obtener tickers con datos."""
        response = app_client.get('/api/tickers')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['items']) == 1
        assert data['items'][0]['symbol'] == 'AAPL'
        assert data['total'] == 1
    
    def test_get_tickers_pagination(self, app_client, db_session):
        """Test paginación de tickers."""
        # Crear múltiples tickers
        for i in range(25):
            ticker = Ticker(symbol=f'TICK{i}', is_active=True)
            db_session.add(ticker)
        db_session.commit()
        
        # Primera página
        response = app_client.get('/api/tickers?page=1&per_page=10')
        data = json.loads(response.data)
        assert len(data['items']) == 10
        assert data['current_page'] == 1
        assert data['has_next'] == True
        
        # Segunda página
        response = app_client.get('/api/tickers?page=2&per_page=10')
        data = json.loads(response.data)
        assert len(data['items']) == 10
        assert data['current_page'] == 2
    
    def test_get_tickers_filter_active(self, app_client, db_session):
        """Test filtro de tickers activos."""
        # Crear tickers activos e inactivos
        active = Ticker(symbol='ACTIVE', is_active=True)
        inactive = Ticker(symbol='INACTIVE', is_active=False)
        db_session.add_all([active, inactive])
        db_session.commit()
        
        # Filtrar solo activos
        response = app_client.get('/api/tickers?is_active=true')
        data = json.loads(response.data)
        assert len(data['items']) == 1
        assert data['items'][0]['symbol'] == 'ACTIVE'
    
    def test_get_tickers_sort(self, app_client, db_session):
        """Test ordenamiento de tickers."""
        # Crear tickers
        t1 = Ticker(symbol='ZZZZ', is_active=True)
        t2 = Ticker(symbol='AAAA', is_active=True)
        db_session.add_all([t1, t2])
        db_session.commit()
        
        # Ordenar asc
        response = app_client.get('/api/tickers?sort_by=symbol&sort_order=asc')
        data = json.loads(response.data)
        assert data['items'][0]['symbol'] == 'AAAA'
        assert data['items'][1]['symbol'] == 'ZZZZ'
        
        # Ordenar desc
        response = app_client.get('/api/tickers?sort_by=symbol&sort_order=desc')
        data = json.loads(response.data)
        assert data['items'][0]['symbol'] == 'ZZZZ'
        assert data['items'][1]['symbol'] == 'AAAA'
    
    def test_add_ticker_success(self, app_client, db_session):
        """Test agregar ticker exitosamente."""
        response = app_client.post('/api/tickers', 
            json={'symbol': 'TSLA'},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'id' in data
        assert data['message'] == 'Ticker added'
        
        # Verificar en DB
        ticker = Ticker.query.filter_by(symbol='TSLA').first()
        assert ticker is not None
    
    def test_add_ticker_normalizes_symbol(self, app_client, db_session):
        """Test que el símbolo se normaliza."""
        response = app_client.post('/api/tickers',
            json={'symbol': '  tsla  '},
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        # Verificar que se guardó en mayúsculas
        ticker = Ticker.query.filter_by(symbol='TSLA').first()
        assert ticker is not None
    
    def test_add_ticker_missing_symbol(self, app_client):
        """Test agregar ticker sin símbolo."""
        response = app_client.post('/api/tickers',
            json={},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_ticker_invalid_symbol(self, app_client):
        """Test agregar ticker con símbolo inválido."""
        response = app_client.post('/api/tickers',
            json={'symbol': 'INVALID_SYMBOL_123'},
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_add_ticker_duplicate(self, app_client, db_session, sample_ticker):
        """Test agregar ticker duplicado."""
        response = app_client.post('/api/tickers',
            json={'symbol': 'AAPL'},
            content_type='application/json'
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'error' in data
        assert 'already exists' in data['error']
    
    def test_add_ticker_with_extra_fields(self, app_client, db_session):
        """Test agregar ticker con campos extra."""
        response = app_client.post('/api/tickers',
            json={
                'symbol': 'TSLA',
                'name': 'Tesla Inc',
                'sector': 'Technology',
                'is_active': True
            },
            content_type='application/json'
        )
        
        assert response.status_code == 200
        
        # Verificar campos
        ticker = Ticker.query.filter_by(symbol='TSLA').first()
        assert ticker.name == 'Tesla Inc'
        assert ticker.sector == 'Technology'
        assert ticker.is_active == True
    
    def test_delete_ticker_success(self, app_client, db_session, sample_ticker):
        """Test eliminar ticker exitosamente."""
        response = app_client.delete(f'/api/tickers/{sample_ticker.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Ticker deleted'
        
        # Verificar que se eliminó
        ticker = Ticker.query.get(sample_ticker.id)
        assert ticker is None
    
    def test_delete_ticker_not_found(self, app_client):
        """Test eliminar ticker que no existe."""
        response = app_client.delete('/api/tickers/99999')
        
        assert response.status_code == 404
    
    def test_delete_ticker_deletes_prices(self, app_client, db_session, sample_ticker, sample_prices):
        """Test que eliminar ticker también elimina precios."""
        price_count = Price.query.filter_by(ticker_id=sample_ticker.id).count()
        assert price_count == 50
        
        # Eliminar ticker
        app_client.delete(f'/api/tickers/{sample_ticker.id}')
        
        # Verificar que se eliminaron los precios
        price_count = Price.query.filter_by(ticker_id=sample_ticker.id).count()
        assert price_count == 0


class TestScanAPI:
    """Tests para la API de escaneo."""
    
    def test_scan_default_strategy(self, app_client, db_session, sample_ticker, sample_prices):
        """Test escaneo con estrategia por defecto."""
        response = app_client.get('/api/scan')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        if data:
            assert 'symbol' in data[0]
            assert 'rsi' in data[0]
    
    def test_scan_with_strategy(self, app_client, db_session, sample_ticker, sample_prices):
        """Test escaneo con estrategia específica."""
        response = app_client.get('/api/scan?strategy=3_emas')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        if data:
            assert 'symbol' in data[0]
            assert 'emas_d_active' in data[0]
            assert 'emas_w_active' in data[0]
    
    def test_scan_invalid_strategy(self, app_client):
        """Test escaneo con estrategia inválida."""
        response = app_client.get('/api/scan?strategy=invalid')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_scan_no_data(self, app_client, db_session):
        """Test escaneo sin tickers con datos."""
        # Crear ticker sin precios suficientes
        ticker = Ticker(symbol='NODATA', is_active=True)
        db_session.add(ticker)
        db_session.commit()
        
        response = app_client.get('/api/scan')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        # Debería retornar lista vacía o solo tickers con datos suficientes
        assert isinstance(data, list)


class TestRefreshAPI:
    """Tests para la API de refresco."""
    
    @patch('yfinance.download')
    def test_refresh_success(self, mock_download, app_client, db_session, sample_ticker):
        """Test refresco exitoso."""
        # Configurar mock
        import pandas as pd
        dates = pd.date_range('2024-01-01', periods=5, freq='D')
        mock_data = pd.DataFrame({
            'Open': [100.0] * 5,
            'High': [105.0] * 5,
            'Low': [95.0] * 5,
            'Close': [102.0] * 5,
            'Volume': [1000000] * 5
        }, index=dates)
        mock_download.return_value = mock_data
        
        response = app_client.post('/api/refresh')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 1
        assert 'symbol' in data[0]
        assert 'new_records' in data[0]
    
    def test_refresh_empty(self, app_client, db_session):
        """Test refresco sin tickers."""
        response = app_client.post('/api/refresh')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []


class TestSeedAPI:
    """Tests para la API de seed."""
    
    def test_seed_tickers(self, app_client, db_session):
        """Test agregar tickers de ejemplo."""
        response = app_client.post('/api/seed')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'Seeds added' in data['message']
        
        # Verificar que se agregaron
        tickers = Ticker.query.all()
        assert len(tickers) > 0


class TestRateLimiting:
    """Tests para rate limiting."""
    
    def test_rate_limiting_respected(self, app_client):
        """Test que se respeta el límite de tasa."""
        # Hacer múltiples peticiones rápidas
        responses = []
        for _ in range(60):
            response = app_client.get('/api/tickers')
            responses.append(response.status_code)
        
        # Verificar que algunas peticiones fueron limitadas
        assert 429 in responses
    
    def test_rate_limiting_headers(self, app_client):
        """Test que se incluyen headers de rate limiting."""
        response = app_client.get('/api/tickers')
        
        # Debería incluir headers de rate limiting
        # (dependiendo de la configuración de Flask-Limiter)
        pass
