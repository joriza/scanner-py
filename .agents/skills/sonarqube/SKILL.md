# SonarQube Skill

## Descripción
Esta habilidad proporciona conocimientos y capacidades para trabajar con SonarQube, una plataforma de análisis continuo de calidad de código. Incluye desde la instalación y configuración hasta la integración en pipelines CI/CD y la interpretación de resultados.

## Requisitos Previos
- Java 11 o superior (para SonarQube)
- Docker (opcional, para despliegue en contenedores)
- Acceso a un servidor SonarQube o capacidad para desplegar uno
- Conocimientos básicos de CI/CD

## Instalación y Configuración

### Instalación con Docker
```bash
# Crear volumen para persistencia
docker volume create sonarqube_data

# Ejecutar SonarQube
docker run -d --name sonarqube \
  -p 9000:9000 \
  -v sonarqube_data:/opt/sonarqube/data \
  sonarqube:latest

# Acceder a http://localhost:9000
# Credenciales por defecto: admin/admin
```

### Instalación Local
```bash
# Descargar SonarQube
wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.9.0.65466.zip

# Descomprimir
unzip sonarqube-9.9.0.65466.zip

# Ejecutar
cd sonarqube-9.9.0.65466/bin/linux-x86-64
./sonar.sh start
```

### Configuración Básica
```bash
# Editar sonar.properties
sonar.jdbc.url=jdbc:postgresql://localhost/sonar
sonar.jdbc.username=sonar
sonar.jdbc.password=sonar
```

## Análisis de Código

### Análisis con SonarScanner CLI
```bash
# Instalar SonarScanner
# Descargar desde https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/

# Ejecutar análisis
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

### Análisis con Maven
```bash
# Agregar a pom.xml
<plugin>
  <groupId>org.sonarsource.scanner.maven</groupId>
  <artifactId>sonar-maven-plugin</artifactId>
  <version>3.9.1.2184</version>
</plugin>

# Ejecutar análisis
mvn sonar:sonar \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

### Análisis con Gradle
```bash
# Agregar a build.gradle
plugins {
  id "org.sonarqube" version "3.3"
}

// Ejecutar análisis
./gradlew sonarqube \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

### Análisis con Python
```bash
# Instalar sonar-scanner
pip install sonar-scanner

# Ejecutar análisis
sonar-scanner \
  -Dsonar.projectKey=my-python-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=your-token
```

## Integración CI/CD

### Jenkins Pipeline
```groovy
pipeline {
  agent any
  stages {
    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('SonarQube') {
          sh 'mvn sonar:sonar'
        }
      }
    }
    stage('Quality Gate') {
      steps {
        timeout(time: 1, unit: 'HOURS') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
  }
}
```

### GitHub Actions
```yaml
name: SonarQube Analysis
on: [push, pull_request]

jobs:
  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
      - name: SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### GitLab CI
```yaml
sonarqube-check:
  image: maven:3.6.3-jdk-11
  variables:
    SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  script:
    - mvn sonar:sonar -Dsonar.projectKey=${CI_PROJECT_NAME}
  allow_failure: true
```

## Configuración de Reglas de Calidad

### Crear Perfil de Calidad Personalizado
1. Navegar a Quality Profiles
2. Crear nuevo perfil basado en uno existente
3. Activar/desactivar reglas según necesidades
4. Asignar perfil al proyecto

### Configurar Quality Gate
1. Navegar a Quality Gates
2. Crear nuevo Quality Gate o editar existente
3. Configurar condiciones:
   - Coverage on New Code > 80%
   - Duplicated Lines on New Code < 3%
   - Maintainability Rating on New Code = A
4. Asignar Quality Gate al proyecto

## Interpretación de Resultados

### Métricas Principales
- **Code Smells**: Problemas de mantenibilidad
- **Bugs**: Defectos potenciales
- **Vulnerabilities**: Problemas de seguridad
- **Coverage**: Porcentaje de código cubierto por tests
- **Duplications**: Porcentaje de código duplicado

### Niveles de Calidad
- **A**: Excelente (0-5% de deuda técnica)
- **B**: Bueno (5-10%)
- **C**: Regular (10-20%)
- **D**: Pobre (20-50%)
- **E**: Crítico (>50%)

## Mejores Prácticas

### Configuración de Análisis
- Analizar solo código nuevo (New Code Period)
- Excluir archivos de prueba y configuración
- Configurar exclusiones específicas por lenguaje

### Integración en Proceso de Desarrollo
- Ejecutar análisis en cada commit
- Configurar Quality Gate para bloquear PRs con problemas
- Revisar y corregir issues regularmente

### Gestión de Deuda Técnica
- Priorizar corrección de bugs y vulnerabilidades
- Planificar reducción de deuda técnica
- Documentar excepciones justificadas

## Troubleshooting Común

### Análisis Falla
```bash
# Ver logs detallados
sonar-scanner -X

# Verificar conexión
curl -u token: http://localhost:9000/api/server/version
```

### Problemas de Memoria
```bash
# Aumentar memoria en sonar.properties
sonar.web.javaOpts=-Xmx2G -Xms1G
sonar.ce.javaOpts=-Xmx2G -Xms1G
```

### Issues No Detectados
- Verificar que el lenguaje esté habilitado
- Confirmar que los archivos estén en el directorio de fuentes
- Revisar exclusiones configuradas

## Recursos Adicionales
- [Documentación Oficial de SonarQube](https://docs.sonarqube.org/)
- [SonarQube Scanner](https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/)
- [SonarQube Plugins](https://docs.sonarqube.org/latest/extend/plugin-development/)
- [SonarSource Blog](https://www.sonarsource.com/blog/)
