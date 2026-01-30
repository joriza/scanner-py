"""
Script de diagnóstico para identificar problemas con la aplicación.
"""

import sys
import os

def check_python_version():
    """Verificar versión de Python."""
    print(f"Python versión: {sys.version}")
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 8):
        print("⚠️  ADVERTENCIA: Python 3.8+ es requerido")
        return False
    return True

def check_dependencies():
    """Verificar dependencias instaladas."""
    print("\nVerificando dependencias...")
    
    required = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'Flask-SQLAlchemy',
        'yfinance': 'yfinance',
        'pandas': 'pandas',
        'pandas_ta': 'pandas-ta',
        'flasgger': 'flasgger',
        'gunicorn': 'gunicorn',
        'requests': 'requests',
        'sqlalchemy': 'SQLAlchemy',
    }
    
    optional = {
        'flask_limiter': 'Flask-Limiter',
        'flask_cors': 'Flask-CORS',
        'marshmallow': 'marshmallow',
        'pythonjsonlogger': 'python-json-logger',
        'prometheus_client': 'prometheus-client',
        'pytest': 'pytest',
        'pytest_cov': 'pytest-cov',
        'pytest_mock': 'pytest-mock',
        'pytest_flask': 'pytest-flask',
    }
    
    all_ok = True
    
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ✗ {package} - NO INSTALADO")
            all_ok = False
    
    print()
    for module, package in optional.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ✗ {package} - NO INSTALADO (opcional)")
    
    return all_ok

def check_files():
    """Verificar archivos del proyecto."""
    print("\nVerificando archivos del proyecto...")
    
    files_to_check = [
        'app.py',
        'database.py',
        'finance_service.py',
        'logging_config.py',
        'schemas.py',
        'metrics.py',
        'tests/__init__.py',
        'tests/conftest.py',
        'pytest.ini',
    ]
    
    for file in files_to_check:
        if os.path.exists(file):
            print(f"  ✅ {file} existe")
        else:
            print(f"  ✗ {file} NO EXISTE")
    
    print()

def check_imports():
    """Verificar importaciones de módulos nuevos."""
    print("\nVerificando importaciones de módulos nuevos...")
    
    modules = [
        ('logging_config', 'logging_config'),
        ('schemas', 'schemas'),
        ('metrics', 'metrics'),
    ]
    
    for module_name, import_path in modules:
        try:
            importlib.import_module(import_path)
            print(f"  ✅ {module_name} se importa correctamente")
        except Exception as e:
            print(f"  ✗ {module_name} ERROR: {e}")
            return False
    
    return True

def check_app_syntax():
    """Verificar sintaxis de app.py."""
    print("\nVerificando sintaxis de app.py...")
    
    try:
        with open('app.py', 'r') as f:
            compile(f.read(), 'app.py', 'exec')
        print("  ✅ app.py no tiene errores de sintaxis")
        return True
    except SyntaxError as e:
        print(f"  ✗ app.py tiene error de sintaxis:")
        print(f"    Línea: {e.lineno}")
        print(f"    Error: {e.msg}")
        return False
    except Exception as e:
        print(f"  ✗ Error al leer app.py: {e}")
        return False

def main():
    """Función principal."""
    print("=" * 60)
    print("DIAGNÓSTICO - SCANNER PRO")
    print("=" * 60)
    print()
    
    # 1. Verificar versión de Python
    if not check_python_version():
        print("\n❌ VERSIÓN DE PYTHON INCOMPATIBLE")
        print("Por favor, instala Python 3.8 o superior")
        sys.exit(1)
    
    # 2. Verificar dependencias requeridas
    deps_ok = check_dependencies()
    
    # 3. Verificar archivos
    check_files()
    
    # 4. Verificar importaciones
    imports_ok = check_imports()
    
    # 5. Verificar sintaxis
    syntax_ok = check_app_syntax()
    
    print()
    print("=" * 60)
    print("RESUMEN")
    print("=" * 60)
    
    if deps_ok and imports_ok and syntax_ok:
        print("\n✅ Todas las verificaciones pasaron exitosamente")
        print("\nPara ejecutar la aplicación:")
        print("  python app.py")
        print("\nPara ejecutar tests:")
        print("  pytest")
    else:
        print("\n❌ HAY PROBLEMAS QUE DEBEN CORREGIRSE")
        print("\nSoluciones sugeridas:")
        
        if not deps_ok:
            print("  1. Instalar dependencias faltantes:")
            print("     pip install -r requirements.txt")
        
        if not imports_ok:
            print("  2. Verificar errores de importación en los módulos nuevos")
        
        if not syntax_ok:
            print("  3. Corregir errores de sintaxis en app.py")

if __name__ == '__main__':
    main()
