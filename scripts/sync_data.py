import requests
import time

print("Iniciando sincronización de datos de tickers...")
print("=" * 60)

try:
    response = requests.post('http://127.0.0.1:5000/api/refresh', timeout=600)
    
    if response.status_code == 200:
        results = response.json()
        print(f"\n✅ Sincronización completada exitosamente!")
        print(f"Total de tickers procesados: {len(results)}\n")
        
        # Contar resultados
        con_datos_nuevos = sum(1 for r in results if r.get('new_records', 0) > 0)
        sin_datos_nuevos = len(results) - con_datos_nuevos
        total_registros = sum(r.get('new_records', 0) for r in results)
        
        print(f"Resumen:")
        print(f"  - Tickers con nuevos datos: {con_datos_nuevos}")
        print(f"  - Tickers sin nuevos datos: {sin_datos_nuevos}")
        print(f"  - Total de registros nuevos: {total_registros}")
        
        # Mostrar detalles de tickers con datos nuevos
        if con_datos_nuevos > 0:
            print(f"\nTickers actualizados:")
            for r in results:
                if r.get('new_records', 0) > 0:
                    print(f"  ✓ {r['symbol']:10} - {r['new_records']} nuevos registros")
        
        # Mostrar tickers que siguen sin datos
        sin_datos = [r['symbol'] for r in results if r.get('new_records', 0) == 0]
        if sin_datos:
            print(f"\nTickers que siguen sin datos ({len(sin_datos)}):")
            for i in range(0, len(sin_datos), 10):
                print(f"  {', '.join(sin_datos[i:i+10])}")
                
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("⏱️  La sincronización está tomando más tiempo del esperado.")
    print("Esto es normal con muchos tickers. Verifica el progreso en los logs de Flask.")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
