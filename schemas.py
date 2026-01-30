"""
Esquemas de validación para Scanner Pro.

Este módulo define los esquemas de validación usando marshmallow
para validar y sanitizar los datos de entrada de la API.
"""

from marshmallow import Schema, fields, validate, validates, ValidationError, pre_load
from datetime import datetime


class TickerSchema(Schema):
    """Esquema para validación de tickers."""
    
    symbol = fields.Str(
        required=True,
        validate=[
            validate.Length(min=1, max=20, error='El símbolo debe tener entre 1 y 20 caracteres'),
            validate.Regexp(
                r'^[A-Z]{1,5}(\.[A-Z]{1,2})?$',
                error='El símbolo debe tener el formato válido (ej: AAPL, BRK.B, TSLA)'
            )
        ],
        error_messages={'required': 'El símbolo es requerido'}
    )
    
    name = fields.Str(
        load_default=None,
        validate=validate.Length(max=100, error='El nombre no puede exceder 100 caracteres')
    )
    
    sector = fields.Str(
        load_default=None,
        validate=validate.Length(max=100, error='El sector no puede exceder 100 caracteres')
    )
    
    is_active = fields.Bool(load_default=True)
    
    @pre_load
    def normalize_symbol(self, data, **kwargs):
        """Normalizar el símbolo antes de la validación."""
        if 'symbol' in data and data['symbol']:
            data['symbol'] = data['symbol'].upper().strip()
        return data


class TickerQuerySchema(Schema):
    """Esquema para validación de parámetros de consulta de tickers."""
    
    page = fields.Int(load_default=1, validate=validate.Range(min=1, error='La página debe ser mayor a 0'))
    per_page = fields.Int(
        load_default=20,
        validate=validate.Range(min=1, max=100, error='per_page debe estar entre 1 y 100')
    )
    is_active = fields.Bool(load_default=None)
    sector = fields.Str(load_default=None)
    sort_by = fields.Str(
        load_default='symbol',
        validate=validate.OneOf(
            ['symbol', 'name', 'sector', 'last_sync', 'created_at'],
            error='sort_by debe ser uno de: symbol, name, sector, last_sync, created_at'
        )
    )
    sort_order = fields.Str(
        load_default='asc',
        validate=validate.OneOf(['asc', 'desc'], error='sort_order debe ser asc o desc')
    )


class ScanQuerySchema(Schema):
    """Esquema para validación de parámetros de escaneo."""
    
    strategy = fields.Str(
        load_default='rsi_macd',
        validate=validate.OneOf(
            ['rsi_macd', '3_emas', 'bollinger_bands', 'stochastic'],
            error='strategy debe ser una de: rsi_macd, 3_emas, bollinger_bands, stochastic'
        )
    )


class AlertSchema(Schema):
    """Esquema para validación de alertas."""
    
    ticker_id = fields.Int(
        required=True,
        validate=validate.Range(min=1, error='ticker_id debe ser mayor a 0'),
        error_messages={'required': 'ticker_id es requerido'}
    )
    
    user_email = fields.Email(
        required=True,
        error_messages={'required': 'user_email es requerido'}
    )
    
    condition = fields.Str(
        required=True,
        validate=validate.OneOf(
            ['rsi_below', 'rsi_above', 'macd_cross', 'price_above', 'price_below'],
            error='condition debe ser una de: rsi_below, rsi_above, macd_cross, price_above, price_below'
        ),
        error_messages={'required': 'condition es requerido'}
    )
    
    threshold = fields.Float(
        required=True,
        error_messages={'required': 'threshold es requerido'}
    )
    
    is_active = fields.Bool(load_default=True)


class LoginSchema(Schema):
    """Esquema para validación de login."""
    
    username = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=50, error='El username debe tener entre 1 y 50 caracteres'),
        error_messages={'required': 'El username es requerido'}
    )
    
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, error='El password debe tener al menos 6 caracteres'),
        error_messages={'required': 'El password es requerido'}
    )


class ValidationErrorResponse:
    """Clase helper para formatear respuestas de error de validación."""
    
    @staticmethod
    def format(errors):
        """
        Formatear errores de validación de marshmallow para la respuesta.
        
        Args:
            errors: Diccionario de errores de marshmallow
            
        Returns:
            Diccionario con el error formateado
        """
        formatted = {}
        for field, messages in errors.items():
            if isinstance(messages, list):
                formatted[field] = messages[0] if messages else 'Error de validación'
            elif isinstance(messages, dict):
                # Manejar recursión sin llamar al mismo método
                for sub_field, sub_messages in messages.items():
                    if isinstance(sub_messages, list):
                        formatted[f"{field}.{sub_field}"] = sub_messages[0] if sub_messages else 'Error de validación'
                    else:
                        formatted[f"{field}.{sub_field}"] = str(sub_messages)
            else:
                formatted[field] = str(messages)
        
        return {'error': formatted}
