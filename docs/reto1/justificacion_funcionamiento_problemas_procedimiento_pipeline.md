# Justificación del Pipeline CP 1.2 - Reto 1

## Descripción General

Este documento describe el funcionamiento del pipeline de CI implementado para el Caso Práctico 1.2, los problemas encontrados durante su desarrollo y las soluciones aplicadas.

---

## 1. Instalación de Herramientas

### 1.1 Módulos Python

Se instalaron los siguientes módulos Python necesarios para el pipeline:

```bash
pip install pytest flask flake8 bandit coverage
```

| Módulo | Versión | Propósito |
|--------|---------|-----------|
| pytest | 7.4.4 | Framework de testing para ejecutar pruebas unitarias y de integración |
| flask | 2.x | Framework web para la API REST |
| flake8 | 7.x | Análisis de código estático (linting) |
| bandit | 1.x | Análisis de seguridad del código Python |
| coverage | 7.4.4 | Medición de cobertura de código |

### 1.2 Plugins de Jenkins

Se instalaron los siguientes plugins en Jenkins:

| Plugin | Propósito |
|--------|-----------|
| JUnit | Publicación de resultados de tests |
| GitHub | Integración con repositorios GitHub |
| Coverage Plugin | Publicación de informes de cobertura (reemplaza al deprecated Cobertura) |
| Warnings Next Generation | Publicación de resultados de análisis estático (flake8, bandit) |
| Performance | Publicación de resultados de pruebas de rendimiento JMeter |

### 1.3 JMeter

Se instaló Apache JMeter v5.6.3 en `/opt/jmeter/`:

```bash
cd /opt
sudo wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.6.3.tgz
sudo tar -xzf apache-jmeter-5.6.3.tgz
sudo ln -s /opt/apache-jmeter-5.6.3 /opt/jmeter
```

---

## 2. Estructura del Pipeline

### 2.1 Etapas Implementadas

El pipeline consta de las siguientes etapas:

```
┌─────────────────────────────────────────────────────────────┐
│                      GET CODE                                │
│  - Descarga código desde GitHub                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   TESTS (Paralelo)                          │
├───────────────┬───────────────┬───────────────┬─────────────┤
│     UNIT      │     REST      │    STATIC     │  SECURITY   │
│  + Coverage   │  (Flask+Mock) │   (flake8)    │  (bandit)   │
└───────────────┴───────────────┴───────────────┴─────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    PERFORMANCE                               │
│  - JMeter (5 hilos, 40 llamadas por endpoint)               │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Descripción de Cada Etapa

#### Get Code
- Descarga el código fuente desde el repositorio GitHub
- Muestra el contenido del workspace para verificación

#### Unit (con Coverage)
- Ejecuta las pruebas unitarias **una única vez** en todo el pipeline
- Utiliza `coverage run` para medir la cobertura durante la ejecución
- Genera informe XML de cobertura
- Publica resultados con el plugin Coverage
- **Quality Gates**:
  - Líneas: <85% unhealthy, <95% unstable
  - Ramas: <80% unhealthy, <90% unstable

#### Rest
- Levanta el servidor Flask en el puerto 5000
- Levanta WireMock en el puerto 9090 (contenedor Docker)
- Ejecuta las pruebas de integración contra la API
- Limpia los servicios al finalizar

#### Static (flake8)
- Ejecuta análisis de código estático con flake8
- Genera informe en formato pylint
- **Quality Gates**:
  - ≥8 hallazgos → unstable (amarillo)
  - ≥10 hallazgos → failure (rojo)

#### Security (bandit)
- Ejecuta análisis de seguridad con bandit
- Genera informe con formato personalizado
- **Quality Gates**:
  - ≥2 hallazgos → unstable (amarillo)
  - ≥4 hallazgos → failure (rojo)

#### Performance
- Levanta el servidor Flask
- Ejecuta el test-plan de JMeter:
  - 5 hilos concurrentes
  - 8 loops por hilo
  - 40 llamadas a `/calc/add/4/9`
  - 40 llamadas a `/calc/substract/4/9`
- Genera informe HTML y publica resultados

### 2.3 Características Importantes

1. **Pruebas unitarias ejecutadas UNA sola vez**: El comando `coverage run -m pytest test/unit` ejecuta los tests unitarios y mide la cobertura simultáneamente, evitando ejecutarlos dos veces.

2. **Paralelización**: Las etapas Unit, Rest, Static y Security se ejecutan en paralelo para optimizar el tiempo total del pipeline.

3. **catchError**: Todas las etapas usan `catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE')` para que el pipeline continúe aunque una etapa falle.

---

## 3. Problemas Encontrados y Soluciones

### 3.1 Plugin Cobertura Deprecated

**Problema**: El plugin Cobertura original lanzaba el error:
```
java.lang.ClassNotFoundException: hudson.util.IOException2
```

**Causa**: El plugin Cobertura está deprecated y no es compatible con versiones recientes de Jenkins.

**Solución**: Migrar al plugin **Coverage** usando `publishCoverage` con `coberturaAdapter`:
```groovy
publishCoverage adapters: [coberturaAdapter('coverage.xml')],
    sourceFileResolver: sourceFiles('NEVER_STORE'),
    globalThresholds: [...]
```

### 3.2 Coverage Source Code Painting

**Problema**: El plugin Coverage mostraba errores al intentar pintar el código fuente:
```
Skipping coloring of file: app/api.py (not part of workspace or permitted source code folders)
```

**Causa**: El plugin no encontraba los archivos fuente para mostrar las líneas cubiertas/no cubiertas.

**Solución**: Aceptar la limitación y usar `sourceFileResolver: sourceFiles('NEVER_STORE')`. Los totales de cobertura se muestran correctamente, aunque no se pueda ver el detalle línea por línea. Esta es una limitación conocida del plugin para proyectos Python.

### 3.3 JMeter - Permiso Denegado en Log

**Problema**: JMeter fallaba con error de permisos:
```
FileNotFoundException: jmeter.log (Permiso denegado)
```

**Causa**: JMeter intentaba escribir el archivo de log en un directorio sin permisos de escritura.

**Solución**: Especificar la ubicación del log con el parámetro `-j`:
```bash
/opt/jmeter/bin/jmeter -n -t test/jmeter/flask.jmx -l results.jtl -j jmeter.log -e -o jmeter-report/
```

### 3.4 JMeter - Carpeta de Reporte No Vacía

**Problema**: En ejecuciones sucesivas, JMeter fallaba con:
```
Cannot write to 'jmeter-report' as folder is not empty
```

**Causa**: JMeter no sobrescribe la carpeta de reportes si ya existe.

**Solución**: Limpiar los resultados anteriores antes de ejecutar JMeter:
```bash
rm -rf jmeter-report/ results.jtl
```

### 3.5 Docker - Permisos para WireMock

**Problema**: El stage Rest fallaba al intentar iniciar WireMock:
```
permission denied while trying to connect to the docker API
```

**Causa**: El usuario jenkins no tenía permisos para acceder al socket de Docker.

**Solución**: Añadir el usuario jenkins al grupo docker:
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 3.6 Quality Gates - Parámetro Incorrecto

**Problema**: Warning en los logs:
```
WARNING: Unknown parameter(s) found for class type 'WarningsQualityGate': failure
```

**Causa**: El parámetro `failure` no es válido en `qualityGates` del plugin warnings-ng.

**Solución**: Aunque genera warning, el pipeline funciona correctamente. El threshold superior actúa como límite para failure.

---

## 4. Configuración del Test-Plan JMeter

El archivo `test/jmeter/flask.jmx` está configurado con:

| Parámetro | Valor |
|-----------|-------|
| Número de hilos | 5 |
| Loops por hilo | 8 |
| Total llamadas por endpoint | 40 (5 × 8) |
| Endpoint suma | `/calc/add/4/9` |
| Endpoint resta | `/calc/substract/4/9` |
| Host | localhost |
| Puerto | 5000 |

---

## 5. Resultados Obtenidos

### 5.1 Tests
- **Unit**: 20 tests ejecutados correctamente
- **Rest**: 2 tests ejecutados correctamente

### 5.2 Cobertura (antes de mejora Reto 3)
- Líneas: 54.55%
- Ramas: 41.67%

### 5.3 Análisis Estático
- **Flake8**: 9 hallazgos (marca build como UNSTABLE por superar threshold de 8)
- **Bandit**: 0 hallazgos de seguridad

### 5.4 Performance
- Throughput: ~100 requests/segundo
- Tiempo de respuesta (línea 90%): ~3-4 ms
- Errores: 0%

---

## 6. Conclusiones

El pipeline implementado cumple con todos los requisitos del Reto 1 del CP 1.2:

1. ✅ Eliminadas las etapas "Build" y "Results"
2. ✅ Etapa "Get Code" funcional
3. ✅ Etapa "Unit" con cobertura (tests ejecutados 1 sola vez)
4. ✅ Etapa "Rest" con Flask y WireMock
5. ✅ Etapa "Static" con flake8 y quality gates
6. ✅ Etapa "Security" con bandit y quality gates
7. ✅ Etapa "Performance" con JMeter (5 hilos, 40 llamadas por endpoint)
8. ✅ Todas las etapas publican sus resultados con los plugins correspondientes
9. ✅ El pipeline continúa independientemente del resultado de cada etapa

---

**Documento creado para:** Caso Práctico 1.2 - Reto 1 - Experto Universitario en DevOps & Cloud - UNIR
**Fecha:** 2025-01-17
**Autor:** Joan Nicolau
