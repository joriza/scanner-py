"""
Métricas de Prometheus para Scanner Pro.

Este módulo define las métricas que serán recolectadas
por Prometheus para monitoreo de la aplicación.
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest
from flask import Response
from datetime import datetime
import time


# Contadores
http_requests_total = Counter(
    'http_requests_total',
    'Total de peticiones HTTP',
    ['method', 'endpoint', 'status']
)

sync_operations_total = Counter(
    'sync_operations_total',
    'Total de operaciones de sincronización',
    ['symbol', 'status']
)

sync_errors_total = Counter(
    'sync_errors_total',
    'Total de errores de sincronización',
    ['symbol', 'error_type']
)

signals_calculated_total = Counter(
    'signals_calculated_total',
    'Total de señales calculadas',
    ['strategy', 'symbol']
)

tickers_added_total = Counter(
    'tickers_added_total',
    'Total de tickers agregados'
)

tickers_deleted_total = Counter(
    'tickers_deleted_total',
    'Total de tickers eliminados'
)

# Histogramas
http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'Duración de peticiones HTTP en segundos',
    ['method', 'endpoint']
)

sync_duration_seconds = Histogram(
    'sync_duration_seconds',
    'Duración de sincronización en segundos',
    ['symbol'],
    buckets=[0.5, 1, 2, 5, 10, 30, 60, 120]
)

signal_calculation_duration_seconds = Histogram(
    'signal_calculation_duration_seconds',
    'Duración del cálculo de señales en segundos',
    ['strategy'],
    buckets=[0.1, 0.5, 1, 2, 5, 10]
)

database_query_duration_seconds = Histogram(
    'database_query_duration_seconds',
    'Duración de consultas a base de datos en segundos',
    ['query_type'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1, 2, 5]
)

# Gauges
active_tickers_count = Gauge(
    'active_tickers_count',
    'Número de tickers activos'
)

total_tickers_count = Gauge(
    'total_tickers_count',
    'Número total de tickers'
)

total_prices_count = Gauge(
    'total_prices_count',
    'Número total de registros de precios'
)

last_sync_timestamp = Gauge(
    'last_sync_timestamp',
    'Timestamp de la última sincronización',
    ['symbol']
)

cache_hits_total = Counter(
    'cache_hits_total',
    'Total de cache hits',
    ['cache_type']
)

cache_misses_total = Counter(
    'cache_misses_total',
    'Total de cache misses',
    ['cache_type']
)


def setup_metrics(app):
    """
    Configurar el middleware de métricas en la aplicación Flask.
    
    Args:
        app: Instancia de Flask
    """
    @app.before_request
    def before_request():
        from flask import g
        g.start_time = time.time()
    
    @app.after_request
    def after_request(response):
        from flask import g, request
        from datetime import datetime
        
        if hasattr(g, 'start_time'):
            if isinstance(g.start_time, (int, float)):
                duration = (datetime.now() - datetime.fromtimestamp(g.start_time)).total_seconds()
            else:
                duration = 0.0
            
            # Registrar métrica de duración
            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.path
            ).observe(duration)
            
            # Registrar métrica de contador
            http_requests_total.labels(
                method=request.method,
                endpoint=request.path,
                status=response.status_code
            ).inc()
        
        return response
    
    @app.route('/metrics')
    def metrics():
        """Endpoint para exponer métricas de Prometheus."""
        return Response(generate_latest(), mimetype='text/plain')


def update_ticker_metrics():
    """
    Actualizar las métricas de tickers.
    Debe llamarse periódicamente o después de cambios.
    """
    from database import db, Ticker, Price
    
    try:
        # Contar tickers activos
        active_count = Ticker.query.filter_by(is_active=True).count()
        active_tickers_count.set(active_count)
        
        # Contar total de tickers
        total_count = Ticker.query.count()
        total_tickers_count.set(total_count)
        
        # Contar total de precios
        prices_count = Price.query.count()
        total_prices_count.set(prices_count)
        
    except Exception as e:
        # Loggear error pero no fallar
        import logging
        logger = logging.getLogger('metrics')
        logger.error(f'Error actualizando métricas de tickers: {e}')


def record_sync_duration(symbol, duration, status='success'):
    """
    Registrar la duración de una sincronización.
    
    Args:
        symbol: Símbolo del ticker
        duration: Duración en segundos
        status: Estado de la sincronización (success/error)
    """
    sync_duration_seconds.labels(symbol=symbol).observe(duration)
    sync_operations_total.labels(symbol=symbol, status=status).inc()


def record_sync_error(symbol, error_type):
    """
    Registrar un error de sincronización.
    
    Args:
        symbol: Símbolo del ticker
        error_type: Tipo de error
    """
    sync_errors_total.labels(symbol=symbol, error_type=error_type).inc()


def record_signal_calculation(strategy, duration, symbol=None):
    """
    Registrar el cálculo de una señal.
    
    Args:
        strategy: Estrategia utilizada
        duration: Duración en segundos
        symbol: Símbolo del ticker (opcional)
    """
    signal_calculation_duration_seconds.labels(strategy=strategy).observe(duration)
    signals_calculated_total.labels(strategy=strategy, symbol=symbol or 'unknown').inc()


def record_cache_hit(cache_type):
    """
    Registrar un cache hit.
    
    Args:
        cache_type: Tipo de caché (lru, redis, etc.)
    """
    cache_hits_total.labels(cache_type=cache_type).inc()


def record_cache_miss(cache_type):
    """
    Registrar un cache miss.
    
    Args:
        cache_type: Tipo de caché (lru, redis, etc.)
    """
    cache_misses_total.labels(cache_type=cache_type).inc()
