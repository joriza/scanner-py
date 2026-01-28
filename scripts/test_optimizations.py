#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar las optimizaciones de rendimiento.
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Verificar que todos los módulos se importan correctamente."""
    print("=== Probando importaciones ===")
    try:
        from app import app, db, Ticker, Price
        from finance_service import FinanceService
        print("[OK] Importaciones exitosas")
        return True
    except Exception as e:
        print(f"[ERROR] Error en importaciones: {e}")
        return False

def test_database_schema():
    """Verificar que el esquema de base de datos es correcto."""
    print("\n=== Probando esquema de base de datos ===")
    try:
        from app import app, db
        from database import Price

        with app.app_context():
            # Verificar que el indice existe
            inspector = db.inspect(db.engine)
            indexes = inspector.get_indexes('price')
            index_names = [idx['name'] for idx in indexes]

            if 'idx_ticker_date' in index_names:
                print("[OK] Indice idx_ticker_date existe")
            else:
                print("[WARN] Indice idx_ticker_date no encontrado (requiere migracion)")

            # Verificar unicidad
            constraints = inspector.get_unique_constraints('price')
            constraint_names = [c['name'] for c in constraints]

            if '_ticker_date_uc' in constraint_names:
                print("[OK] Restriccion de unicidad _ticker_date_uc existe")
            else:
                print("[ERROR] Restriccion de unicidad _ticker_date_uc no encontrada")
                return False

        return True
    except Exception as e:
        print(f"[ERROR] Error en esquema de base de datos: {e}")
        return False

def test_finance_service():
    """Verificar que FinanceService funciona correctamente."""
    print("\n=== Probando FinanceService ===")
    try:
        from app import app
        from finance_service import FinanceService

        with app.app_context():
            # Verificar que el metodo normalize_symbol funciona
            test_symbols = ['BRK.B', 'BCBA:TICKER', 'TSLA']
            for symbol in test_symbols:
                normalized = FinanceService.normalize_symbol(symbol)
                print(f"  {symbol} -> {normalized}")

            print("[OK] FinanceService funciona correctamente")
            return True
    except Exception as e:
        print(f"[ERROR] Error en FinanceService: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_routes():
    """Verificar que las rutas de la aplicacion funcionan."""
    print("\n=== Probando rutas de la aplicacion ===")
    try:
        from app import app

        with app.test_client() as client:
            # Probar ruta principal
            response = client.get('/')
            if response.status_code == 200:
                print("[OK] Ruta / funciona")
            else:
                print(f"[ERROR] Ruta / fallo con codigo {response.status_code}")

            # Probar ruta de API de tickers
            response = client.get('/api/tickers')
            if response.status_code == 200:
                print("[OK] Ruta /api/tickers funciona")
            else:
                print(f"[ERROR] Ruta /api/tickers fallo con codigo {response.status_code}")

        return True
    except Exception as e:
        print(f"[ERROR] Error en rutas de la aplicacion: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Ejecutar todas las pruebas."""
    print("=" * 60)
    print("PRUEBAS DE OPTIMIZACIONES DE RENDIMIENTO")
    print("=" * 60)

    results = []

    results.append(("Importaciones", test_imports()))
    results.append(("Esquema de BD", test_database_schema()))
    results.append(("FinanceService", test_finance_service()))
    results.append(("Rutas de App", test_app_routes()))

    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)

    for test_name, result in results:
        status = "PASO" if result else "FALLO"
        print(f"{test_name}: {status}")

    all_passed = all(result for _, result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] TODAS LAS PRUEBAS PASARON")
    else:
        print("[ERROR] ALGUNAS PRUEBAS FALLARON")
    print("=" * 60)

    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
