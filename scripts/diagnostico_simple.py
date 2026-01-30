"""
Script de diagnóstico simple para identificar problemas con la aplicación.
"""

import sys
import os

def main():
    print("=" * 60)
    print("DIAGNÓSTICO - SCANNER PRO")
    print("=" * 60)
    print()
    
    # 1. Verificar versión de Python
    print(f"Python versión: {sys.version}")
    print()
    
    # 2. Verificar dependencias
    print("Verificando dependencias...")
    deps = ['flask', 'flask_sqlalchemy', 'yfinance', 'pandas', 'pandas_ta', 'flasgger', 'gunicorn', 'requests', 'sqlalchemy']
    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            print(f"  ✗ {dep} - NO INSTALADO")
    print()
    
    # 3. Verificar archivos nuevos
    print("Verificando archivos nuevos...")
    new_files = ['logging_config.py', 'schemas.py', 'metrics.py', 'pytest.ini']
    for file in new_files:
        if os.path.exists(file):
            print(f"  ✅ {file} existe")
        else:
            print(f"  ✗ {file} NO EXISTE")
    print()
    
    # 4. Verificar sintaxis de app.py
    print("Verificando sintaxis de app.py...")
    try:
        with open('app.py', 'r') as f:
            compile(f.read(), 'app.py', 'exec')
        print("  ✅ app.py - sintaxis OK")
    except SyntaxError as e:
        print(f"  ✗ app.py - ERROR DE SINTAXIS: {e}")
    except Exception as e:
        print(f"  ✗ app.py - ERROR: {e}")
    print()
    
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    print()
    
    print("Si todas las verificaciones pasaron, ejecuta:")
    print("  python app.py")
    print()
    print("Si hay errores, revisa:")
    print("  1. Instala dependencias: pip install -r requirements.txt")
    print("  2. Verifica que los archivos nuevos existen")
    print("  3. Revisa el traceback de error en la terminal")

if __name__ == '__main__':
    main()
