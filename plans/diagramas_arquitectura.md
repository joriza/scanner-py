# Diagramas de Arquitectura - Mejoras Propuestas

**Fecha:** 29 de enero de 2026
**Relacionado con:** [`mejoras_propuestas.md`](mejoras_propuestas.md)

## Arquitectura Actual vs Propuesta

### Arquitectura Actual

```mermaid
graph TB
    subgraph Cliente
        A[Dashboard Web]
        B[Panel Admin]
    end
    
    subgraph Flask App
        C[app.py]
        D[API Routes]
        E[FinanceService]
        F[database.py]
    end
    
    subgraph Datos
        G[SQLite DB]
        H[yfinance API]
    end
    
    A --> C
    B --> C
    D --> E
    D --> F
    E --> H
    F --> G
    
    style A fill:#e1f5ff
    style B fill:#e1f5ff
    style C fill:#fff4e1
    style E fill:#fff4e1
    style F fill:#fff4e1
    style G fill:#ffe1f5
    style H fill:#e1ffe1
```

### Arquitectura Propuesta con Mejoras

```mermaid
graph TB
    subgraph Cliente
        A[Dashboard Web]
        B[Panel Admin]
        C[WebSocket Client]
    end
    
    subgraph Seguridad
        D[Rate Limiter]
        E[CORS Middleware]
        F[JWT Auth]
        G[Input Validation]
    end
    
    subgraph Flask App
        H[app.py]
        I[API Routes v1/v2]
        J[FinanceService]
        K[database.py]
        L[Events System]
        M[Notification Service]
    end
    
    subgraph Monitoreo
        N[Health Check]
        O[Prometheus Metrics]
        P[Structured Logging]
        Q[Tracing]
    end
    
    subgraph Datos
        R[PostgreSQL/SQLite]
        S[yfinance API]
        T[Redis Cache]
    end
    
    subgraph DevOps
        U[Docker Container]
        V[CI/CD Pipeline]
        W[Backup System]
    end
    
    subgraph Testing
        X[Unit Tests]
        Y[Integration Tests]
        Z[Performance Tests]
    end
    
    A --> D
    B --> D
    C --> H
    D --> E
    E --> F
    F --> G
    G --> I
    I --> J
    I --> K
    I --> L
    J --> S
    K --> R
    L --> M
    M --> A
    M --> C
    H --> N
    H --> O
    H --> P
    H --> Q
    J --> T
    H --> U
    U --> V
    V --> W
    X --> H
    Y --> H
    Z --> H
    
    style A fill:#e1f5ff
    style B fill:#e1f5ff
    style C fill:#e1f5ff
    style D fill:#ffcccc
    style E fill:#ffcccc
    style F fill:#ffcccc
    style G fill:#ffcccc
    style H fill:#fff4e1
    style I fill:#fff4e1
    style J fill:#fff4e1
    style K fill:#fff4e1
    style L fill:#fff4e1
    style M fill:#fff4e1
    style N fill:#ccffcc
    style O fill:#ccffcc
    style P fill:#ccffcc
    style Q fill:#ccffcc
    style R fill:#ffe1f5
    style S fill:#e1ffe1
    style T fill:#ffe1f5
    style U fill:#ffccff
    style V fill:#ffccff
    style W fill:#ffccff
    style X fill:#ffffcc
    style Y fill:#ffffcc
    style Z fill:#ffffcc
```

---

## Diagrama de Capas con Mejoras

```mermaid
graph TB
    subgraph Capa de Presentacion
        A1[Dashboard Web]
        A2[Panel Admin]
        A3[API Documentation]
        A4[WebSocket Client]
    end
    
    subgraph Capa de Seguridad
        B1[Rate Limiting]
        B2[CORS]
        B3[JWT Authentication]
        B4[Input Validation]
        B5[Data Sanitization]
    end
    
    subgraph Capa de Aplicacion
        C1[API Routes v1]
        C2[API Routes v2]
        C3[FinanceService]
        C4[Events System]
        C5[Notification Service]
        C6[Cache Manager]
    end
    
    subgraph Capa de Negocio
        D1[Signal Calculation]
        D2[Data Synchronization]
        D3[Alert Processing]
        D4[Strategy Engine]
    end
    
    subgraph Capa de Datos
        E1[PostgreSQL/SQLite]
        E2[Redis Cache]
        E3[Alembic Migrations]
        E4[Backup System]
    end
    
    subgraph Capa de Integracion
        F1[yfinance API]
        F2[Email Service]
        F3[Webhook Service]
    end
    
    subgraph Capa de Infraestructura
        G1[Docker Container]
        G2[Kubernetes]
        G3[Load Balancer]
        G4[CDN]
    end
    
    subgraph Capa de Monitoreo
        H1[Health Checks]
        H2[Prometheus Metrics]
        H3[Structured Logging]
        H4[Distributed Tracing]
        H5[Alert Manager]
    end
    
    subgraph Capa de Testing
        I1[Unit Tests]
        I2[Integration Tests]
        I3[E2E Tests]
        I4[Performance Tests]
    end
    
    subgraph Capa de CI/CD
        J1[GitHub Actions]
        J2[Automated Builds]
        J3[Automated Tests]
        J4[Automated Deployments]
        J5[Rollback System]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    B5 --> C1
    B5 --> C2
    C1 --> C3
    C2 --> C3
    C3 --> C4
    C3 --> C5
    C3 --> C6
    C3 --> D1
    C3 --> D2
    C3 --> D3
    C3 --> D4
    D1 --> E1
    D2 --> E1
    D3 --> E1
    D4 --> E1
    C3 --> E2
    E1 --> E3
    E1 --> E4
    D2 --> F1
    C5 --> F2
    C4 --> F3
    H --> G1
    G1 --> G2
    G2 --> G3
    G3 --> G4
    C3 --> H1
    C3 --> H2
    C3 --> H3
    C3 --> H4
    H2 --> H5
    I1 --> C3
    I2 --> C3
    I3 --> C3
    I4 --> C3
    J1 --> J2
    J2 --> J3
    J3 --> J4
    J4 --> J5
    J4 --> G1
    
    style A1 fill:#e1f5ff
    style A2 fill:#e1f5ff
    style A3 fill:#e1f5ff
    style A4 fill:#e1f5ff
    style B1 fill:#ffcccc
    style B2 fill:#ffcccc
    style B3 fill:#ffcccc
    style B4 fill:#ffcccc
    style B5 fill:#ffcccc
    style C1 fill:#fff4e1
    style C2 fill:#fff4e1
    style C3 fill:#fff4e1
    style C4 fill:#fff4e1
    style C5 fill:#fff4e1
    style C6 fill:#fff4e1
    style D1 fill:#ffe1cc
    style D2 fill:#ffe1cc
    style D3 fill:#ffe1cc
    style D4 fill:#ffe1cc
    style E1 fill:#ffe1f5
    style E2 fill:#ffe1f5
    style E3 fill:#ffe1f5
    style E4 fill:#ffe1f5
    style F1 fill:#e1ffe1
    style F2 fill:#e1ffe1
    style F3 fill:#e1ffe1
    style G1 fill:#ffccff
    style G2 fill:#ffccff
    style G3 fill:#ffccff
    style G4 fill:#ffccff
    style H1 fill:#ccffcc
    style H2 fill:#ccffcc
    style H3 fill:#ccffcc
    style H4 fill:#ccffcc
    style H5 fill:#ccffcc
    style I1 fill:#ffffcc
    style I2 fill:#ffffcc
    style I3 fill:#ffffcc
    style I4 fill:#ffffcc
    style J1 fill:#ccffff
    style J2 fill:#ccffff
    style J3 fill:#ccffff
    style J4 fill:#ccffff
    style J5 fill:#ccffff
```

---

## Flujo de Datos con Mejoras

### Flujo de Sincronización Mejorado

```mermaid
sequenceDiagram
    participant C as Cliente
    participant RL as Rate Limiter
    participant Auth as JWT Auth
    participant API as API Route
    participant FS as FinanceService
    participant Cache as Redis Cache
    participant YF as yfinance API
    participant DB as Database
    participant Events as Events System
    participant Notif as Notification Service
    participant Metrics as Prometheus
    
    C->>RL: POST /api/refresh
    RL->>Auth: Verificar rate limit
    Auth->>API: Validar token JWT
    API->>FS: sync_all_tickers()
    
    loop Para cada ticker
        FS->>Cache: Verificar caché
        alt Caché hit
            Cache-->>FS: Datos en caché
        else Caché miss
            FS->>YF: Descargar datos
            YF-->>FS: Datos históricos
            FS->>DB: Guardar precios
            DB-->>FS: Confirmación
            FS->>Cache: Guardar en caché
        end
        FS->>Events: Emitir evento ticker_synced
        Events->>Metrics: Registrar métricas
        Events->>Notif: Verificar alertas
        alt Alerta activada
            Notif->>C: Enviar email notificación
        end
    end
    
    FS-->>API: Resultados
    API->>Metrics: Registrar duración
    API-->>C: JSON con resultados
```

### Flujo de Consulta de Señales con Caché

```mermaid
sequenceDiagram
    participant C as Cliente
    participant WS as WebSocket
    participant API as API Route
    participant Cache as LRU Cache
    participant FS as FinanceService
    participant DB as Database
    participant Metrics as Prometheus
    
    C->>WS: Conectar WebSocket
    WS-->>C: Conexión establecida
    
    C->>API: GET /api/scan?strategy=rsi_macd
    API->>Cache: Verificar caché (ticker_id, strategy)
    
    alt Caché hit
        Cache-->>API: Señales en caché
        API->>Metrics: Registrar cache hit
    else Caché miss
        API->>FS: get_signals(ticker, strategy)
        FS->>DB: Consultar precios
        DB-->>FS: Datos de precios
        FS->>FS: Calcular indicadores
        FS-->>API: Señales calculadas
        API->>Cache: Guardar en caché
        API->>Metrics: Registrar cache miss
    end
    
    API-->>C: JSON con señales
    
    Note over WS,C: Actualización en tiempo real
    Events->>WS: Emitir señal actualizada
    WS-->>C: Actualizar dashboard
```

---

## Diagrama de Despliegue con Mejoras

```mermaid
graph TB
    subgraph Usuario
        U1[Navegador Web]
        U2[Cliente API]
    end
    
    subgraph CDN
        CDN1[CloudFlare/CloudFront]
    end
    
    subgraph Load Balancer
        LB[NGINX/HAProxy]
    end
    
    subgraph Kubernetes Cluster
        subgraph Pod 1
            APP1[Scanner App]
            REDIS1[Redis Cache]
        end
        
        subgraph Pod 2
            APP2[Scanner App]
            REDIS2[Redis Cache]
        end
        
        subgraph Pod 3
            APP3[Scanner App]
            REDIS3[Redis Cache]
        end
        
        subgraph Database
            PG[PostgreSQL]
            BACKUP[Backup System]
        end
    end
    
    subgraph Monitoreo
        PROM[Prometheus]
        GRAF[Grafana]
        ALERT[AlertManager]
        JAEGER[Jaeger Tracing]
    end
    
    subgraph CI/CD
        GH[GitHub Actions]
        REG[Docker Registry]
    end
    
    U1 --> CDN1
    U2 --> CDN1
    CDN1 --> LB
    LB --> APP1
    LB --> APP2
    LB --> APP3
    APP1 --> REDIS1
    APP2 --> REDIS2
    APP3 --> REDIS3
    APP1 --> PG
    APP2 --> PG
    APP3 --> PG
    PG --> BACKUP
    APP1 --> PROM
    APP2 --> PROM
    APP3 --> PROM
    PROM --> GRAF
    PROM --> ALERT
    APP1 --> JAEGER
    APP2 --> JAEGER
    APP3 --> JAEGER
    GH --> REG
    REG --> APP1
    REG --> APP2
    REG --> APP3
    
    style U1 fill:#e1f5ff
    style U2 fill:#e1f5ff
    style CDN1 fill:#ccffcc
    style LB fill:#ffcccc
    style APP1 fill:#fff4e1
    style APP2 fill:#fff4e1
    style APP3 fill:#fff4e1
    style REDIS1 fill:#ffe1f5
    style REDIS2 fill:#ffe1f5
    style REDIS3 fill:#ffe1f5
    style PG fill:#ffe1f5
    style BACKUP fill:#ffe1f5
    style PROM fill:#ccffcc
    style GRAF fill:#ccffcc
    style ALERT fill:#ccffcc
    style JAEGER fill:#ccffcc
    style GH fill:#ffffcc
    style REG fill:#ffffcc
```

---

## Diagrama de Testing con Mejoras

```mermaid
graph TB
    subgraph Desarrollo
        DEV[Desarrollador]
        GIT[Git Repository]
    end
    
    subgraph CI/CD Pipeline
        GH[GitHub Actions]
        LINT[Linting]
        UNIT[Unit Tests]
        INT[Integration Tests]
        PERF[Performance Tests]
        BUILD[Docker Build]
        DEPLOY[Deploy to Staging]
    end
    
    subgraph Staging Environment
        STAGE_APP[App Instance]
        STAGE_DB[Test Database]
        STAGE_TESTS[E2E Tests]
    end
    
    subgraph Production Environment
        PROD_APP[App Instance]
        PROD_DB[Production DB]
        MON[Monitoreo]
    end
    
    DEV --> GIT
    GIT --> GH
    GH --> LINT
    LINT --> UNIT
    UNIT --> INT
    INT --> PERF
    PERF --> BUILD
    BUILD --> DEPLOY
    DEPLOY --> STAGE_APP
    STAGE_APP --> STAGE_DB
    STAGE_APP --> STAGE_TESTS
    STAGE_TESTS --> PROD_APP
    PROD_APP --> PROD_DB
    PROD_APP --> MON
    
    style DEV fill:#e1f5ff
    style GIT fill:#fff4e1
    style GH fill:#ffffcc
    style LINT fill:#ffcccc
    style UNIT fill:#ccffcc
    style INT fill:#ccffcc
    style PERF fill:#ccffcc
    style BUILD fill:#ffccff
    style DEPLOY fill:#ffccff
    style STAGE_APP fill:#ffe1f5
    style STAGE_DB fill:#ffe1f5
    style STAGE_TESTS fill:#ffe1f5
    style PROD_APP fill:#ffe1f5
    style PROD_DB fill:#ffe1f5
    style MON fill:#ccffcc
```

---

## Diagrama de Seguridad con Mejoras

```mermaid
graph TB
    subgraph Cliente
        USER[Usuario]
        BROWSER[Navegador]
    end
    
    subgraph Capa de Seguridad Perimetral
        WAF[Web Application Firewall]
        DDoS[DDoS Protection]
        CDN[CDN with SSL]
    end
    
    subgraph Capa de Seguridad de Aplicación
        CORS[CORS Policy]
        RATE[Rate Limiter]
        AUTH[JWT Authentication]
        AUTHZ[Authorization]
        VALID[Input Validation]
        SANIT[Data Sanitization]
    end
    
    subgraph Capa de Seguridad de Datos
        ENCRYPT[Encryption at Rest]
        TLS[TLS 1.3]
        BACKUP[Encrypted Backups]
    end
    
    subgraph Capa de Monitoreo de Seguridad
        AUDIT[Audit Logging]
        ALERT[Security Alerts]
        SIEM[SIEM Integration]
    end
    
    subgraph Aplicación
        APP[Flask App]
        API[API Endpoints]
        DB[Database]
    end
    
    USER --> BROWSER
    BROWSER --> WAF
    WAF --> DDoS
    DDoS --> CDN
    CDN --> CORS
    CORS --> RATE
    RATE --> AUTH
    AUTH --> AUTHZ
    AUTHZ --> VALID
    VALID --> SANIT
    SANIT --> API
    API --> APP
    APP --> DB
    DB --> ENCRYPT
    ENCRYPT --> BACKUP
    API --> TLS
    TLS --> APP
    API --> AUDIT
    AUDIT --> ALERT
    ALERT --> SIEM
    
    style USER fill:#e1f5ff
    style BROWSER fill:#e1f5ff
    style WAF fill:#ffcccc
    style DDoS fill:#ffcccc
    style CDN fill:#ffcccc
    style CORS fill:#ffcccc
    style RATE fill:#ffcccc
    style AUTH fill:#ffcccc
    style AUTHZ fill:#ffcccc
    style VALID fill:#ffcccc
    style SANIT fill:#ffcccc
    style ENCRYPT fill:#ffcccc
    style TLS fill:#ffcccc
    style BACKUP fill:#ffcccc
    style AUDIT fill:#ccffcc
    style ALERT fill:#ccffcc
    style SIEM fill:#ccffcc
    style APP fill:#fff4e1
    style API fill:#fff4e1
    style DB fill:#ffe1f5
```

---

## Diagrama de Configuración por Ambiente

```mermaid
graph TB
    subgraph Configuracion Base
        BASE[Config Base]
    end
    
    subgraph Desarrollo
        DEV[Development Config]
        DEV1[SQLite DB]
        DEV2[Debug Mode ON]
        DEV3[Local Logging]
    end
    
    subgraph Testing
        TEST[Testing Config]
        TEST1[In-Memory DB]
        TEST2[Debug Mode OFF]
        TEST3[Mock Services]
    end
    
    subgraph Staging
        STAGE[Staging Config]
        STAGE1[PostgreSQL]
        STAGE2[Debug Mode OFF]
        STAGE3[Structured Logging]
        STAGE4[Test Data]
    end
    
    subgraph Produccion
        PROD[Production Config]
        PROD1[PostgreSQL]
        PROD2[Debug Mode OFF]
        PROD3[Structured Logging]
        PROD4[Redis Cache]
        PROD5[JWT Secret]
        PROD6[Email Config]
    end
    
    BASE --> DEV
    BASE --> TEST
    BASE --> STAGE
    BASE --> PROD
    DEV --> DEV1
    DEV --> DEV2
    DEV --> DEV3
    TEST --> TEST1
    TEST --> TEST2
    TEST --> TEST3
    STAGE --> STAGE1
    STAGE --> STAGE2
    STAGE --> STAGE3
    STAGE --> STAGE4
    PROD --> PROD1
    PROD --> PROD2
    PROD --> PROD3
    PROD --> PROD4
    PROD --> PROD5
    PROD --> PROD6
    
    style BASE fill:#fff4e1
    style DEV fill:#ccffcc
    style TEST fill:#ffffcc
    style STAGE fill:#ffccff
    style PROD fill:#ffcccc
```

---

## Diagrama de Flujo de Eventos

```mermaid
graph LR
    subgraph Eventos
        E1[ticker_added]
        E2[ticker_synced]
        E3[ticker_deleted]
        E4[sync_error]
        E5[signal_alert]
    end
    
    subgraph Suscriptores
        S1[Email Notifier]
        S2[WebSocket Broadcaster]
        S3[Metrics Collector]
        S4[Audit Logger]
        S5[Alert Manager]
    end
    
    subgraph Acciones
        A1[Enviar Email]
        A2[Broadcast WebSocket]
        A3[Registrar Métrica]
        A4[Log Auditoría]
        A5[Disparar Alerta]
    end
    
    E1 --> S1
    E1 --> S3
    E1 --> S4
    E2 --> S2
    E2 --> S3
    E3 --> S3
    E3 --> S4
    E4 --> S1
    E4 --> S3
    E4 --> S5
    E5 --> S1
    E5 --> S2
    E5 --> S5
    
    S1 --> A1
    S2 --> A2
    S3 --> A3
    S4 --> A4
    S5 --> A5
    
    style E1 fill:#e1f5ff
    style E2 fill:#e1f5ff
    style E3 fill:#e1f5ff
    style E4 fill:#e1f5ff
    style E5 fill:#e1f5ff
    style S1 fill:#fff4e1
    style S2 fill:#fff4e1
    style S3 fill:#fff4e1
    style S4 fill:#fff4e1
    style S5 fill:#fff4e1
    style A1 fill:#ccffcc
    style A2 fill:#ccffcc
    style A3 fill:#ccffcc
    style A4 fill:#ccffcc
    style A5 fill:#ccffcc
```

---

## Resumen de Componentes Nuevos

| Componente | Categoría | Prioridad | Complejidad |
|-------------|-----------|-----------|-------------|
| Rate Limiter | Seguridad | 🔴 Alta | Baja |
| CORS Middleware | Seguridad | 🔴 Alta | Baja |
| JWT Authentication | Seguridad | 🟡 Media | Media |
| Input Validation | Seguridad | 🔴 Alta | Media |
| Redis Cache | Datos | 🟡 Media | Media |
| Events System | Arquitectura | 🟢 Baja | Media |
| Notification Service | Funcionalidad | 🟡 Media | Media |
| Health Checks | Monitoreo | 🔴 Alta | Baja |
| Prometheus Metrics | Monitoreo | 🟡 Media | Media |
| Structured Logging | Monitoreo | 🔴 Alta | Media |
| Alembic Migrations | Base de Datos | 🔴 Alta | Media |
| Backup System | Base de Datos | 🟡 Media | Media |
| Unit Tests | Testing | 🔴 Alta | Media |
| Integration Tests | Testing | 🟡 Media | Media |
| Docker Multi-Stage | DevOps | 🔴 Alta | Media |
| GitHub Actions CI/CD | DevOps | 🟡 Media | Media |
| WebSocket | Funcionalidad | 🟢 Baja | Media |
| Email Service | Funcionalidad | 🟡 Media | Media |

---

**Documento creado por:** Roo (Architect Mode)
**Fecha de creación:** 29 de enero de 2026
**Relacionado con:** [`mejoras_propuestas.md`](mejoras_propuestas.md)
