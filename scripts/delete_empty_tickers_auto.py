import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import app
from database import db, Ticker, Price

print("=" * 70)
print("IDENTIFICACIÓN Y ELIMINACIÓN DE TICKERS SIN DATOS")
print("=" * 70)

with app.app_context():
    # Obtener todos los tickers
    all_tickers = Ticker.query.all()
    total_tickers = len(all_tickers)
    
    print(f"\nTotal de tickers en la base de datos: {total_tickers}\n")
    
    # Identificar tickers sin datos
    tickers_sin_datos = []
    tickers_con_datos = []
    
    for ticker in all_tickers:
        price_count = Price.query.filter_by(ticker_id=ticker.id).count()
        if price_count == 0:
            tickers_sin_datos.append(ticker)
        else:
            tickers_con_datos.append((ticker, price_count))
    
    print(f"Tickers sin datos encontrados: {len(tickers_sin_datos)}")
    print(f"Tickers con datos: {len(tickers_con_datos)}\n")
    
    if tickers_sin_datos:
        print("Tickers sin datos a eliminar:")
        for ticker in tickers_sin_datos:
            print(f"  - {ticker.symbol}")
        
        print("\n" + "-" * 70)
        print("Eliminando tickers sin datos...")
        print("-" * 70)
        
        eliminados = 0
        for ticker in tickers_sin_datos:
            db.session.delete(ticker)
            print(f"  [OK] {ticker.symbol:15} - Eliminado")
            eliminados += 1
        
        # Confirmar cambios
        db.session.commit()
        
        print("\n" + "=" * 70)
        print("RESUMEN")
        print("=" * 70)
        print(f"[OK] Tickers eliminados:     {eliminados}")
        print(f"[INFO] Tickers restantes:     {Ticker.query.count()}")
        print("=" * 70)
    else:
        print("\n[OK] No se encontraron tickers sin datos.")
        print(f"[INFO] Todos los {total_tickers} tickers tienen datos.")
        print("=" * 70)
