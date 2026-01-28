import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import db, Ticker, Price

with app.app_context():
    tickers_to_delete = ["DESP", "SQ", "WBA"]
    
    print(f"\nEliminando {len(tickers_to_delete)} tickers deslistados...\n")
    print("=" * 70)
    
    for symbol in tickers_to_delete:
        # Buscar el ticker
        ticker = Ticker.query.filter_by(symbol=symbol).first()
        
        if ticker:
            # Eliminar precios asociados primero
            price_count = Price.query.filter_by(ticker_id=ticker.id).count()
            Price.query.filter_by(ticker_id=ticker.id).delete()
            
            # Eliminar el ticker
            db.session.delete(ticker)
            db.session.commit()
            
            print(f"  [OK] {symbol:8} - {price_count} registros de precios eliminados")
        else:
            print(f"  [X] {symbol:8} - No encontrado en la base de datos")
    
    print("=" * 70)
    print(f"\nProceso completado.\n")
