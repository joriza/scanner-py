"""
Configuración de logging estructurado para Scanner Pro.

Este módulo configura logging con formato JSON para mejor análisis
e integración con herramientas de log aggregation.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from datetime import datetime


def setup_logging(app, level=logging.INFO):
    """
    Configurar logging estructurado con JSON para la aplicación Flask.
    
    Args:
        app: Instancia de Flask
        level: Nivel de logging (default: logging.INFO)
    """
    # Crear handler para stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Configurar formatter JSON
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(name)s %(levelname)s %(message)s %(pathname)s %(lineno)d',
        timestamp=True
    )
    handler.setFormatter(formatter)
    
    # Configurar logger de Flask
    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(level)
    
    # Configurar logger de finance_service
    finance_logger = logging.getLogger('finance_service')
    finance_logger.handlers.clear()
    finance_logger.addHandler(handler)
    finance_logger.setLevel(level)
    
    # Configurar logger raíz
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(level)
    
    # Evitar logs duplicados
    app.logger.propagate = False
    finance_logger.propagate = False


def get_logger(name):
    """
    Obtener un logger con el nombre especificado.
    
    Args:
        name: Nombre del logger
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


class RequestLogger:
    """Middleware para logging de peticiones HTTP."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger('http')
        self.init_app(app)
    
    def init_app(self, app):
        """Inicializar el middleware en la aplicación Flask."""
        @app.before_request
        def before_request():
            from flask import g
            g.start_time = datetime.now()
        
        @app.after_request
        def after_request(response):
            from flask import g, request
            
            if hasattr(g, 'start_time'):
                elapsed = (datetime.now() - g.start_time).total_seconds()
                
                log_data = {
                    'method': request.method,
                    'path': request.path,
                    'status_code': response.status_code,
                    'duration_seconds': elapsed,
                    'remote_addr': request.remote_addr,
                    'user_agent': request.user_agent.string if request.user_agent else None,
                }
                
                # Agregar user_id si está disponible (para autenticación futura)
                if hasattr(g, 'user_id'):
                    log_data['user_id'] = g.user_id
                
                self.logger.info('HTTP request', extra=log_data)
            
            return response


class ErrorLogger:
    """Middleware para logging de errores."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger('error')
        self.init_app(app)
    
    def init_app(self, app):
        """Inicializar el middleware en la aplicación Flask."""
        @app.errorhandler(400)
        def bad_request(error):
            self.logger.warning('Bad request', extra={
                'error': str(error),
                'status_code': 400
            })
            return {'error': str(error)}, 400
        
        @app.errorhandler(404)
        def not_found(error):
            self.logger.warning('Not found', extra={
                'path': error.description if hasattr(error, 'description') else None,
                'status_code': 404
            })
            return {'error': 'Not found'}, 404
        
        @app.errorhandler(500)
        def internal_error(error):
            self.logger.error('Internal server error', extra={
                'error': str(error),
                'status_code': 500
            }, exc_info=True)
            return {'error': 'Internal server error'}, 500
