from app import app
from database import db, Ticker, Price

with app.app_context():
    total_tickers = Ticker.query.count()
    print(f"\n{'='*60}")
    print(f"TOTAL DE TICKERS EN LA BASE DE DATOS: {total_tickers}")
    print(f"{'='*60}\n")
    
    tickers = Ticker.query.all()
    tickers_con_datos = 0
    tickers_sin_datos = 0
    tickers_insuficientes = 0
    
    print("DETALLE DE TICKERS:\n")
    for t in tickers:
        price_count = Price.query.filter_by(ticker_id=t.id).count()
        status = ""
        if price_count == 0:
            status = "❌ SIN DATOS"
            tickers_sin_datos += 1
        elif price_count < 30:
            status = f"⚠️  INSUFICIENTES ({price_count} registros, se necesitan 30+)"
            tickers_insuficientes += 1
        else:
            status = f"✅ OK ({price_count} registros)"
            tickers_con_datos += 1
            
        print(f"  {t.symbol:10} - {status}")
    
    print(f"\n{'='*60}")
    print(f"RESUMEN:")
    print(f"  ✅ Tickers con datos suficientes (30+): {tickers_con_datos}")
    print(f"  ⚠️  Tickers con datos insuficientes (<30): {tickers_insuficientes}")
    print(f"  ❌ Tickers sin datos: {tickers_sin_datos}")
    print(f"{'='*60}\n")
    
    print("RAZÓN POR LA QUE NO SE MUESTRAN TODOS:")
    print("  La función get_signals() en finance_service.py retorna None")
    print("  si un ticker tiene menos de 30 registros de precios (línea 63):")
    print("  'if not prices or len(prices) < 30: return None'")
    print(f"{'='*60}\n")
