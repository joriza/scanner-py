import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from database import db, Ticker

with app.app_context():
    symbol = "RBLX"
    name = "Roblox Corporation"
    sector = "Technology"
    
    # Verificar si el ticker ya existe
    existing = Ticker.query.filter_by(symbol=symbol).first()
    
    if existing:
        print(f"El ticker {symbol} ya existe en la base de datos")
    else:
        # Crear nuevo ticker
        ticker = Ticker(
            symbol=symbol,
            name=name,
            sector=sector,
            is_active=True
        )
        db.session.add(ticker)
        db.session.commit()
        print(f"Ticker {symbol} agregado correctamente")
        print(f"  Nombre: {name}")
        print(f"  Sector: {sector}")
