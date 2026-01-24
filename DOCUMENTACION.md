# Documentación Técnica Detallada - Scanner Pro

## 1. Arquitectura del Sistema
El sistema es una aplicación web full-stack ligera diseñada para el análisis técnico de activos financieros.
- **Backend**: Python 3.x con Flask.
- **Base de Datos**: SQLite (`scanner.db`) administrada con SQLAlchemy.
- **Procesamiento Técnico**: Pandas y Pandas-TA.
- **Frontend**: Dashboard dinámico estructurado en HTML5/CSS3 (Glassmorphism) y Javascript nativo.

## 2. Modelado de Datos
El sistema utiliza dos tablas principales para minimizar el consumo de API externa:
- **Ticker**: Almacena el símbolo y la fecha de la última sincronización.
- **Price**: Almacena `date`, `open`, `high`, `low`, `close` y `volume`. Garantiza que solo se descarguen datos nuevos de forma incremental.

## 3. Definición Detallada de Estrategias

### 🟢 Estrategia 1: 1-RSI+MACD
Optimizado para "Bottom Fishing" (pesca de mínimos).
- **RSI (14 períodos)**:
    - **Sobreventa**: Se busca el evento `RSI < 30` en una ventana de 365 días hacia atrás.
    - **Rebote Confirmado**: Evento `RSI > SMA(RSI, 14)`. Se reporta la **primera vez** que esto sucede después de haber salido de sobreventa.
- **MACD (12, 26, 9)**:
    - **Zona de Compra**: Cruce alcista (`MACD > Signal`) siempre que `MACD <= 0`.
    - **Lógica de Salida (Color Rojo)**: La oportunidad se marca como inactiva si el cruce se vuelve bajista O si el MACD supera la línea de `0`, indicando que el activo ha perdido su condición de "oportunidad de precio bajo".

### 🔵 Estrategia 2: 2-3_EMAS (Diaria + Semanal)
Estrategia de seguimiento de tendencia basada en momentum acumulado.
- **Medias Utilizadas**: EMAs de 4, 9 y 18 períodos.
- **Condición**: `Precio Cierre > EMA 4 AND Precio Cierre > EMA 9 AND Precio Cierre > EMA 18`.
- **Análisis Multi-Timeframe**:
    - **Diario**: Reacción rápida al precio.
    - **Semanal**: Filtro de tendencia mayor. Los datos se recalculan usando resampling de viernes (`W-FRI`). El valor reportado se limita a la fecha de hoy para evitar etiquetas futuras.

## 4. Algoritmo de Ordenamiento Selectivo
El Dashboard no ordena de forma alfabética, sino por **Relevancia Operativa**:

### Para Estrategia 2 (3 EMAS):
Se aplica un sistema de **Jerarquía por Desempate**:
1.  **Nivel 1 (Score)**: `(Activo en Diario + Activo en Semanal)`. Los que suman 2 puntos van primero.
2.  **Nivel 2 (Semanal)**: Entre los que tienen el mismo score, se ordena por días desde el cruce semanal (Menor a Mayor).
3.  **Nivel 3 (Diario - Desempate)**: Si la fecha semanal coincide, se ordena por días desde el cruce diario (Menor a Mayor).
    *   *Ejemplo*: Si A y B tienen 1 día semanal, pero A tiene 1 día diario y B tiene 2 días diarios, **A aparecerá primero**.

## 5. API Backend (Interoperabilidad)
Endpoints disponibles para integración:
- `GET /api/tickers`: Lista todos los activos.
- `POST /api/tickers`: Agrega un activo (normaliza automáticamente puntos por guiones para yfinance).
- `POST /api/refresh`: Sincroniza precios faltantes desde Yahoo Finance.
- `GET /api/scan?strategy=[id]`: Ejecuta el motor de cálculo y devuelve señales en JSON.
- `DELETE /api/tickers/[id]`: Elimina activo y su historial.

## 6. Configuración del Agente (.agent)
El archivo `.agent` en la raíz contiene las reglas de oro para futuros desarrollos, incluyendo la prohibición de uso de placeholders y la obligación de mantener la estética premium en el Dashboard.
