from app import app
from database import db, Ticker, Price

# Lista de tickers sin datos para eliminar
tickers_sin_datos = [
    'RLBX', 'ERJ', 'AMM', 
    'BCBA:CAPX', 'BCBA:COME', 'BCBA:GGAL', 'BCBA:IRSA', 'BCBA:TGNO4', 'BCBA:TGSU2',
    'DESP', 'SQ', 'TXR', 'WBA'
]

print("=" * 70)
print("ELIMINACIÓN DE TICKERS SIN DATOS")
print("=" * 70)
print(f"\nTickers a eliminar: {len(tickers_sin_datos)}\n")

with app.app_context():
    eliminados = 0
    no_encontrados = 0
    
    for symbol in tickers_sin_datos:
        ticker = Ticker.query.filter_by(symbol=symbol).first()
        
        if ticker:
            # Eliminar precios asociados (aunque no deberían tener)
            price_count = Price.query.filter_by(ticker_id=ticker.id).count()
            if price_count > 0:
                Price.query.filter_by(ticker_id=ticker.id).delete()
                print(f"  ✓ {symbol:15} - Eliminado (tenía {price_count} precios)")
            else:
                print(f"  ✓ {symbol:15} - Eliminado")
            
            db.session.delete(ticker)
            eliminados += 1
        else:
            print(f"  ⚠ {symbol:15} - No encontrado en la BD")
            no_encontrados += 1
    
    # Confirmar cambios
    db.session.commit()
    
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(f"✅ Tickers eliminados:     {eliminados}")
    print(f"⚠️  Tickers no encontrados: {no_encontrados}")
    print(f"\nTotal de tickers restantes: {Ticker.query.count()}")
    print("=" * 70)
