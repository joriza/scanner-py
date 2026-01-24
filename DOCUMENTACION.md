# Documentación Técnica: Stock Scanner Pro v1.2.0

## 1. Resumen Ejecutivo
Stock Scanner Pro es una plataforma analítica de alta performance diseñada para el monitoreo cuantitativo de activos financieros. El sistema integra algoritmos de análisis técnico multi-temporal (Daily/Weekly) para identificar patrones de capitulación y momentum, permitiendo a los usuarios filtrar universos de activos mediante reglas estricta de jerarquización operativa.

---

## 2. Pila Tecnológica (Tech Stack)

### 2.1 Backend Core
- **Lenguaje**: Python 3.10+
- **Framework Web**: Flask (WSGI compliant).
- **ORM**: SQLAlchemy para la gestión de la persistencia de datos relacionales.
- **Engine Técnico**: 
  - `Pandas`: Estructuras de datos matriciales (DataFrames).
  - `Pandas-TA`: Biblioteca de análisis técnico para cálculos vectorizados de indicadores.

### 2.2 Persistencia de Datos
- **Motor**: SQLite 3.
- **Modelo Relacional**:
  - `Ticker`: Entidad maestra de activos. Implementa normalización automática de símbolos (ej. conversión de `BCBA:TICKER` a `TICKER.BA`).
  - `Price`: Serie temporal histórica. Almacena OHLCV (Open, High, Low, Close, Volume).

### 2.3 Frontend & Visualización
- **Arquitectura**: Single Page Application (SPA) basada en componentes nativos (Vanilla JS).
- **UI/UX**: Estética Dark-Premium con efectos de Glassmorphism (CSS Moderno).
- **Export Engine**: Integración con `SheetJS` (XLSX) para procesamiento de reportes del lado del cliente.

---

## 3. Lógica Cuantitativa y Estrategias

### 3.1 Estrategia 1: RSI + MACD Momentum Rebound
Diseñada para la detección de reversiones en zonas de agotamiento de venta.

*   **Indicador RSI (p=14)**:
    - **Trigger de Captura**: Localiza el evento `RSI < 30` en una ventana retrospectiva de 365 días.
    - **Señal de Rebote**: Identifica el primer punto de inflexión donde `RSI > SMA(RSI, 14)` posterior al trigger de captura.
*   **Indicador MACD (12, 26, 9)**:
    - **Filtro de Oportunidad**: Cruce alcista (`MACD > Signal`) condicionado a que el valor absoluto del MACD se encuentre en terreno negativo o neutro (`MACD <= 0`).
    - **Invalidación (Exit Strategy)**: La señal conmuta a estado `Inactive` (Visual: Red) de forma inmediata si el cruce se vuelve bajista o si el indicador supera el umbral de `0`.

### 3.2 Estrategia 2: 3-EMA Multi-Timeframe Alignment (4, 9, 18)
Estrategia de seguimiento de tendencia que busca la alineación de momentum en diferentes horizontes temporales.

*   **Parámetros**: Medias Móviles Exponenciales (EMA) de corto (p=4), medio (p=9) y largo (p=18) recorrido.
*   **Alineación Diaria (D)**: Validada mediante `Close > EMA4, EMA9, EMA18`.
*   **Alineación Semanal (W)**: 
    - **Algoritmo de Resampling**: Transforma la serie diaria en semanal utilizando el alias `W-FRI` (Weekly ending on Fridays).
    - **Seguridad de Datos**: El índice temporal se limita estrictamente a la fecha actual (`Capped Logic`) para prevenir la generación de etiquetas futuras y asegurar la integridad de los días transcurridos.

---

## 4. Gestión de Trazabilidad y Ordenamiento

El sistema implementa un algoritmo de **Ordenamiento Jerárquico por Desempate (Hierarchical Sorting)** para la Estrategia 2, asegurando que los activos con mayor fuerza relativa encabecen el listado:

1.  **Prioridad de Alineación (Score)**: `(D_Active + W_Active)`. Puntuación máxima = 2.
2.  **Jerarquía Temporal Mayor**: Ante igualdad de score, se prioriza el activo con el cruce **Semanal** más reciente (ASC).
3.  **Jerarquía de Micro-Momentum**: Ante igualdad en la señal semanal, se desempata por el cruce **Diario** más reciente (ASC).

---

## 5. Capacidades de Interoperabilidad

### 5.1 API RESTful
- `GET /api/scan?strategy=[id]`: Motor de escaneo bajo demanda. Devuelve estructura JSON enriquecida con metadatos técnicos.
- `POST /api/refresh`: Sincronización asíncrona incremental con Yahoo Finance API.
- `POST /api/tickers`: Punto de entrada para nuevos activos con normalización inteligente BCBA/Standard.

### 5.2 Exportación de Datos (Data Portability)
El sistema permite la exportación íntegra del estado actual del dashboard a formato XLSX. Los archivos generados incluyen una nomenclatura estricta: `[StrategyName]_[YYYY-MM-DD_HH-MM].xlsx`.

---

## 6. Mantenimiento y Extensibilidad (AI Ready)

- **Dependency Management**: El entorno de ejecución se rige por el archivo `requirements.txt`.
- **Contexto de Agente**: El archivo `.agent` define las invariantes del sistema, prohibiendo expresamente el uso de datos sintéticos (placeholders) y garantizando la coherencia estilística en futuras expansiones.
- **Versionado**: Gestión de ramas por fecha (ISO 8601) para asegurar la trazabilidad de features.
