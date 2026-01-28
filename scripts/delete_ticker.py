import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import db, Ticker, Price

with app.app_context():
    symbol = 'TRX'
    
    # Buscar el ticker
    ticker = Ticker.query.filter_by(symbol=symbol).first()
    
    if ticker:
        print(f"Eliminando ticker {symbol}...")
        
        # Eliminar precios asociados primero
        price_count = Price.query.filter_by(ticker_id=ticker.id).count()
        Price.query.filter_by(ticker_id=ticker.id).delete()
        print(f"  - {price_count} registros de precios eliminados")
        
        # Eliminar el ticker
        db.session.delete(ticker)
        db.session.commit()
        
        print(f"  - Ticker {symbol} eliminado correctamente")
    else:
        print(f"El ticker {symbol} no existe en la base de datos")
