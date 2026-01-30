"""
Tests unitarios para los esquemas de validación.
"""

import pytest
from marshmallow import ValidationError

from schemas import (
    TickerSchema,
    TickerQuerySchema,
    ScanQuerySchema,
    AlertSchema,
    LoginSchema,
    ValidationErrorResponse
)


class TestTickerSchema:
    """Tests para el esquema de validación de tickers."""
    
    def test_valid_ticker_symbol(self):
        """Test validación de símbolo válido."""
        schema = TickerSchema()
        data = {'symbol': 'AAPL'}
        result = schema.load(data)
        
        assert result['symbol'] == 'AAPL'
    
    def test_symbol_normalization(self):
        """Test normalización de símbolo."""
        schema = TickerSchema()
        data = {'symbol': '  aapl  '}
        result = schema.load(data)
        
        assert result['symbol'] == 'AAPL'
    
    def test_symbol_with_dot(self):
        """Test validación de símbolo con punto."""
        schema = TickerSchema()
        data = {'symbol': 'BRK.B'}
        result = schema.load(data)
        
        assert result['symbol'] == 'BRK.B'
    
    def test_symbol_too_long(self):
        """Test validación de símbolo muy largo."""
        schema = TickerSchema()
        data = {'symbol': 'TOOLONGSYMBOL'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'symbol' in errors
    
    def test_symbol_empty(self):
        """Test validación de símbolo vacío."""
        schema = TickerSchema()
        data = {'symbol': ''}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'symbol' in errors
    
    def test_symbol_missing(self):
        """Test validación de símbolo faltante."""
        schema = TickerSchema()
        data = {}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'symbol' in errors
    
    def test_symbol_invalid_format(self):
        """Test validación de símbolo con formato inválido."""
        schema = TickerSchema()
        data = {'symbol': 'INVALID_123'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'symbol' in errors
    
    def test_optional_fields(self):
        """Test campos opcionales."""
        schema = TickerSchema()
        data = {'symbol': 'TSLA'}
        result = schema.load(data)
        
        assert result['symbol'] == 'TSLA'
        assert result.get('name') is None
        assert result.get('sector') is None
        assert result.get('is_active') == True  # valor por defecto
    
    def test_all_fields(self):
        """Test con todos los campos."""
        schema = TickerSchema()
        data = {
            'symbol': 'TSLA',
            'name': 'Tesla Inc',
            'sector': 'Technology',
            'is_active': False
        }
        result = schema.load(data)
        
        assert result['symbol'] == 'TSLA'
        assert result['name'] == 'Tesla Inc'
        assert result['sector'] == 'Technology'
        assert result['is_active'] == False
    
    def test_name_too_long(self):
        """Test validación de nombre muy largo."""
        schema = TickerSchema()
        data = {
            'symbol': 'AAPL',
            'name': 'A' * 101  # más de 100 caracteres
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'name' in errors
    
    def test_sector_too_long(self):
        """Test validación de sector muy largo."""
        schema = TickerSchema()
        data = {
            'symbol': 'AAPL',
            'sector': 'A' * 101  # más de 100 caracteres
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'sector' in errors


class TestTickerQuerySchema:
    """Tests para el esquema de consulta de tickers."""
    
    def test_default_values(self):
        """Test valores por defecto."""
        schema = TickerQuerySchema()
        data = {}
        result = schema.load(data)
        
        assert result['page'] == 1
        assert result['per_page'] == 20
        assert result['sort_by'] == 'symbol'
        assert result['sort_order'] == 'asc'
    
    def test_pagination_params(self):
        """Test parámetros de paginación."""
        schema = TickerQuerySchema()
        data = {'page': 2, 'per_page': 50}
        result = schema.load(data)
        
        assert result['page'] == 2
        assert result['per_page'] == 50
    
    def test_page_too_low(self):
        """Test validación de página muy baja."""
        schema = TickerQuerySchema()
        data = {'page': 0}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'page' in errors
    
    def test_per_page_too_high(self):
        """Test validación de per_page muy alto."""
        schema = TickerQuerySchema()
        data = {'per_page': 101}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'per_page' in errors
    
    def test_sort_by_valid(self):
        """Test ordenamiento por campo válido."""
        schema = TickerQuerySchema()
        data = {'sort_by': 'name'}
        result = schema.load(data)
        
        assert result['sort_by'] == 'name'
    
    def test_sort_by_invalid(self):
        """Test ordenamiento por campo inválido."""
        schema = TickerQuerySchema()
        data = {'sort_by': 'invalid_field'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'sort_by' in errors
    
    def test_sort_order_valid(self):
        """Test orden de clasificación válido."""
        schema = TickerQuerySchema()
        data = {'sort_order': 'desc'}
        result = schema.load(data)
        
        assert result['sort_order'] == 'desc'
    
    def test_sort_order_invalid(self):
        """Test orden de clasificación inválido."""
        schema = TickerQuerySchema()
        data = {'sort_order': 'invalid'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'sort_order' in errors
    
    def test_is_active_filter(self):
        """Test filtro is_active."""
        schema = TickerQuerySchema()
        data = {'is_active': True}
        result = schema.load(data)
        
        assert result['is_active'] == True
    
    def test_sector_filter(self):
        """Test filtro de sector."""
        schema = TickerQuerySchema()
        data = {'sector': 'Technology'}
        result = schema.load(data)
        
        assert result['sector'] == 'Technology'


class TestScanQuerySchema:
    """Tests para el esquema de consulta de escaneo."""
    
    def test_default_strategy(self):
        """Test estrategia por defecto."""
        schema = ScanQuerySchema()
        data = {}
        result = schema.load(data)
        
        assert result['strategy'] == 'rsi_macd'
    
    def test_valid_strategies(self):
        """Test estrategias válidas."""
        schema = ScanQuerySchema()
        
        valid_strategies = ['rsi_macd', '3_emas', 'bollinger_bands', 'stochastic']
        
        for strategy in valid_strategies:
            data = {'strategy': strategy}
            result = schema.load(data)
            assert result['strategy'] == strategy
    
    def test_invalid_strategy(self):
        """Test estrategia inválida."""
        schema = ScanQuerySchema()
        data = {'strategy': 'invalid_strategy'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'strategy' in errors


class TestAlertSchema:
    """Tests para el esquema de alertas."""
    
    def test_valid_alert(self):
        """Test alerta válida."""
        schema = AlertSchema()
        data = {
            'ticker_id': 1,
            'user_email': 'test@example.com',
            'condition': 'rsi_below',
            'threshold': 30.0
        }
        result = schema.load(data)
        
        assert result['ticker_id'] == 1
        assert result['user_email'] == 'test@example.com'
        assert result['condition'] == 'rsi_below'
        assert result['threshold'] == 30.0
    
    def test_missing_required_fields(self):
        """Test campos requeridos faltantes."""
        schema = AlertSchema()
        data = {}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'ticker_id' in errors
        assert 'user_email' in errors
        assert 'condition' in errors
        assert 'threshold' in errors
    
    def test_invalid_email(self):
        """Test email inválido."""
        schema = AlertSchema()
        data = {
            'ticker_id': 1,
            'user_email': 'invalid_email',
            'condition': 'rsi_below',
            'threshold': 30.0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'user_email' in errors
    
    def test_invalid_condition(self):
        """Test condición inválida."""
        schema = AlertSchema()
        data = {
            'ticker_id': 1,
            'user_email': 'test@example.com',
            'condition': 'invalid_condition',
            'threshold': 30.0
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'condition' in errors
    
    def test_is_active_default(self):
        """Test valor por defecto de is_active."""
        schema = AlertSchema()
        data = {
            'ticker_id': 1,
            'user_email': 'test@example.com',
            'condition': 'rsi_below',
            'threshold': 30.0
        }
        result = schema.load(data)
        
        assert result['is_active'] == True


class TestLoginSchema:
    """Tests para el esquema de login."""
    
    def test_valid_login(self):
        """Test login válido."""
        schema = LoginSchema()
        data = {
            'username': 'admin',
            'password': 'securepassword123'
        }
        result = schema.load(data)
        
        assert result['username'] == 'admin'
        assert result['password'] == 'securepassword123'
    
    def test_missing_username(self):
        """Test username faltante."""
        schema = LoginSchema()
        data = {'password': 'securepassword123'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'username' in errors
    
    def test_missing_password(self):
        """Test password faltante."""
        schema = LoginSchema()
        data = {'username': 'admin'}
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'password' in errors
    
    def test_password_too_short(self):
        """Test password muy corto."""
        schema = LoginSchema()
        data = {
            'username': 'admin',
            'password': '12345'  # menos de 6 caracteres
        }
        
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)
        
        errors = exc_info.value.messages
        assert 'password' in errors


class TestValidationErrorResponse:
    """Tests para el helper de respuesta de error."""
    
    def test_format_simple_errors(self):
        """Test formato de errores simples."""
        errors = {
            'symbol': ['This field is required.'],
            'name': ['Not a valid string.']
        }
        
        result = ValidationErrorResponse.format(errors)
        
        assert 'error' in result
        assert result['error']['symbol'] == 'This field is required.'
        assert result['error']['name'] == 'Not a valid string.'
    
    def test_format_nested_errors(self):
        """Test formato de errores anidados."""
        errors = {
            'user': {
                'email': ['Invalid email.'],
                'password': ['Too short.']
            }
        }
        
        result = ValidationErrorResponse.format(errors)
        
        assert 'error' in result
        assert result['error']['user']['email'] == 'Invalid email.'
        assert result['error']['user']['password'] == 'Too short.'
    
    def test_format_mixed_errors(self):
        """Test formato de errores mixtos."""
        errors = {
            'symbol': ['Required.'],
            'user': {
                'email': ['Invalid.']
            }
        }
        
        result = ValidationErrorResponse.format(errors)
        
        assert 'error' in result
        assert result['error']['symbol'] == 'Required.'
        assert result['error']['user']['email'] == 'Invalid.'
