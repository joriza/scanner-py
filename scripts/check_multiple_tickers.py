import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yfinance as yf
from datetime import datetime, timedelta

def check_ticker_status(symbol):
    """Verifica si un ticker está deslistado o tiene datos recientes."""
    try:
        ticker = yf.Ticker(symbol)
        
        # Verificar si el ticker tiene datos recientes
        today = datetime.now().date()
        
        # Intentar obtener datos históricos
        hist = ticker.history(period="2mo", timeout=30)
        
        if hist.empty:
            return False, 0, None
        
        # Verificar la fecha del último dato
        last_date = hist.index[-1].date()
        days_since_last = (today - last_date).days
        
        return True, days_since_last, last_date
            
    except Exception as e:
        return False, 0, None

if __name__ == "__main__":
    tickers = ["DESP", "SQ", "TRX", "WBA"]
    
    print(f"\nVerificando estado de {len(tickers)} tickers...\n")
    print("=" * 70)
    
    results = []
    for symbol in tickers:
        has_data, days_since, last_date = check_ticker_status(symbol)
        
        if has_data:
            status = "ACTIVO" if days_since <= 30 else "POCO ACTIVO"
            print(f"  [OK] {symbol:8} - {status} - Ultimo dato: {last_date} (hace {days_since} dias)")
            results.append((symbol, "VALIDO"))
        else:
            print(f"  [X] {symbol:8} - SIN DATOS (posiblemente deslistado)")
            results.append((symbol, "DESLISTADO"))
    
    print("=" * 70)
    print("\nResumen:")
    for symbol, status in results:
        print(f"  {symbol}: {status}")
    print()
