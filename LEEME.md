# Guia de Uso - Stock Scanner Pro

La aplicación ya está instalada y configurada en `c:\Users\USER\Desarrollo\scanner-py`.

## Cómo iniciar la aplicación

1.  Abre una terminal (PowerShell).
2.  Navega a la carpeta del proyecto:
    ```powershell
    cd c:\Users\USER\Desarrollo\scanner-py
    ```
3.  Activa el entorno virtual:
    ```powershell
    .\venv\Scripts\activate
    ```
4.  Inicia el servidor:
    ```powershell
    python -m flask run --port=5000
    ```
5.  Abre tu navegador en: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Funcionalidades Actuales (Etapa 1)

### Dashboard Principal
- **Actualizar Precios**: Descarga los datos más recientes de Yahoo Finance de forma incremental.
- **Escanear Indicadores**: Calcula RSI y MACD para mostrar las señales solicitadas.
- **Señales**:
    - **RSI < 30**: Indica cuántos días han pasado desde la última vez que la acción estuvo sobrevendida (último año).
    - **Tendencia RSI**: Indica si el RSI está por encima de su media móvil (Alcista).
    - **MACD Opportunity**: Detecta cruces positivos de MACD ocurriendo por debajo de cero en los últimos 30 días.

### Administración (ABM)
- Permite agregar nuevos Tickers (ej: AAPL, TSLA, BTC-USD).
- Los símbolos se normalizan automáticamente (ej: `BRK.B` a `BRK-B`).
- Permite eliminar tickers y limpiar su historial de la base de datos local.

## Notas Técnicas
- **Base de Datos**: Los precios se guardan en `scanner.db` para evitar descargas repetitivas.
- **Indicadores**: Se calculan al vuelo cada vez que escaneas, garantizando que siempre uses las fórmulas más actualizadas sin ensuciar la base de datos.
- **Frecuencia**: La Etapa 1 está optimizada para temporalidad **Diaria**.
