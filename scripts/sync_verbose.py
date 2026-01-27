from app import app
from database import db, Ticker
from finance_service import FinanceService
import time

print("=" * 70)
print("SINCRONIZACIÓN DE DATOS DE TICKERS")
print("=" * 70)

with app.app_context():
    tickers = Ticker.query.all()
    total = len(tickers)
    
    print(f"\nTotal de tickers a procesar: {total}")
    print(f"Inicio: {time.strftime('%H:%M:%S')}\n")
    
    con_datos_nuevos = 0
    sin_datos_nuevos = 0
    total_registros = 0
    errores = []
    
    for idx, ticker in enumerate(tickers, 1):
        print(f"[{idx}/{total}] Procesando {ticker.symbol:12} ... ", end='', flush=True)
        
        try:
            start_time = time.time()
            count = FinanceService.sync_ticker_data(ticker)
            elapsed = time.time() - start_time
            
            if count > 0:
                print(f"✅ {count:4} nuevos registros ({elapsed:.1f}s)")
                con_datos_nuevos += 1
                total_registros += count
            else:
                print(f"⚪ Sin nuevos datos ({elapsed:.1f}s)")
                sin_datos_nuevos += 1
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)[:50]}")
            errores.append((ticker.symbol, str(e)))
        
        # Mostrar resumen cada 20 tickers
        if idx % 20 == 0:
            print(f"\n--- Progreso: {idx}/{total} ({idx*100//total}%) ---")
            print(f"    Actualizados: {con_datos_nuevos} | Sin cambios: {sin_datos_nuevos} | Errores: {len(errores)}")
            print(f"    Total registros nuevos: {total_registros}\n")
    
    print("\n" + "=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    print(f"Fin: {time.strftime('%H:%M:%S')}")
    print(f"\n✅ Tickers actualizados:     {con_datos_nuevos}")
    print(f"⚪ Tickers sin nuevos datos: {sin_datos_nuevos}")
    print(f"❌ Tickers con errores:      {len(errores)}")
    print(f"📊 Total registros nuevos:   {total_registros}")
    
    if errores:
        print(f"\nErrores encontrados ({len(errores)}):")
        for symbol, error in errores[:10]:  # Mostrar solo los primeros 10
            print(f"  • {symbol}: {error[:60]}")
        if len(errores) > 10:
            print(f"  ... y {len(errores) - 10} más")
    
    print("=" * 70)
