import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yfinance as yf
from datetime import datetime, timedelta

def check_ticker_status(symbol):
    """Verifica si un ticker está deslistado o tiene datos recientes."""
    try:
        ticker = yf.Ticker(symbol)
        
        # Intentar obtener información básica
        info = ticker.info
        
        # Verificar si el ticker tiene datos recientes
        today = datetime.now().date()
        two_months_ago = today - timedelta(days=60)
        
        # Intentar obtener datos históricos
        hist = ticker.history(period="2mo", timeout=30)
        
        if hist.empty:
            print(f"  [X] {symbol}: SIN DATOS (posiblemente deslistado)")
            return False
        
        # Verificar la fecha del último dato
        last_date = hist.index[-1].date()
        days_since_last = (today - last_date).days
        
        if days_since_last > 30:
            print(f"  [!] {symbol}: Ultimo dato hace {days_since_last} dias ({last_date.strftime('%Y-%m-%d')}) - POSIBLEMENTE DESLISTADO")
            return False
        else:
            print(f"  [OK] {symbol}: Activo - Ultimo dato hace {days_since_last} dias ({last_date.strftime('%Y-%m-%d')})")
            return True
            
    except Exception as e:
        print(f"  [X] {symbol}: Error al verificar - {str(e)}")
        return False

if __name__ == "__main__":
    symbol = "AMM"
    print(f"\nVerificando estado del ticker {symbol}...\n")
    is_valid = check_ticker_status(symbol)
    print(f"\nResultado: {'VALIDO' if is_valid else 'DESLISTADO/INVALIDO'}\n")
