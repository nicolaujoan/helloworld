# Justificación de la Distribución de Agentes

## Contexto

Este documento justifica la estrategia de distribución de agentes Jenkins para los pipelines de CI/CD del proyecto HelloWorld, tanto para el CP 1.1 como para el CP 1.2.

## Recursos Disponibles

- **Master**: Nodo controlador de Jenkins (coordinación)
- **Agent1**: Nodo worker para ejecución de tareas
- **Agent2**: Nodo worker para ejecución de tareas

**Total: 3 nodos disponibles**

---

## CP 1.1 - Distribución de Agentes

### Etapas del Pipeline CP 1.1

1. **Get Code**: Descarga del código fuente desde GitHub
2. **Unit**: Pruebas unitarias con pytest
3. **Rest**: Pruebas de integración (requiere Flask + WireMock)
4. **Results**: Publicación de resultados con JUnit

### Distribución Implementada

```
┌─────────────────────────────────────────────────┐
│ Get Code (Master - implícito)                   │
│ - git clone                                     │
│ - stash código                                  │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ Tests (Paralelo)                                │
├────────────────────┬────────────────────────────┤
│ Unit (Agent1)      │ Rest (Agent2)              │
│ - unstash código   │ - unstash código           │
│ - pytest unit      │ - start Flask              │
│ - stash resultados │ - start WireMock           │
│                    │ - pytest rest              │
│                    │ - stop servicios           │
│                    │ - stash resultados         │
└────────────────────┴────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│ Results (Master - implícito)                    │
│ - unstash resultados Unit y Rest                │
│ - junit 'result*.xml'                           │
└─────────────────────────────────────────────────┘
```

### Justificación CP 1.1

**Decisión:** Paralelizar las pruebas Unit y Rest en agentes separados (agent1 y agent2).

**Razones:**

1. ✅ **Máxima paralelización**: Con solo 2 tipos de pruebas paralelas y 2 agentes workers, se aprovechan al máximo los recursos disponibles.

2. ✅ **Aislamiento de recursos**:
   - Unit en agent1: Trabajo CPU-intensivo (ejecución de tests)
   - Rest en agent2: Trabajo I/O-intensivo (servicios Flask + WireMock + tests)

3. ✅ **Evita conflictos**: Al ejecutar Rest en un agente dedicado, se evitan conflictos de puertos (Flask en 5000, WireMock en 9090) con otras tareas.

4. ✅ **Optimización del master**: El master se reserva para tareas de coordinación (Get Code y Results), que son ligeras y rápidas.

5. ✅ **Reducción del tiempo total**: El tiempo de ejecución es igual al tiempo de la etapa más lenta (en lugar de la suma de ambas).

**Alternativas consideradas y descartadas:**

- ❌ **Ejecutar todo en master**: Desaprovecha los agentes y no hay paralelización.
- ❌ **Ejecutar todo en un solo agente**: No hay paralelización, tiempo total mayor.
- ❌ **Usar master para Unit o Rest**: Sobrecarga el nodo controlador, mala práctica.

**Conclusión CP 1.1:** La distribución actual es **óptima** para los recursos disponibles.

---

## CP 1.2 - Distribución de Agentes

### Etapas del Pipeline CP 1.2

1. **Get Code**: Descarga del código fuente
2. **Unit**: Pruebas unitarias (⚠️ **solo puede ejecutarse 1 vez**)
3. **Rest**: Pruebas de integración (requiere Flask + WireMock)
4. **Static**: Análisis estático con flake8
5. **Security**: Análisis de seguridad con bandit
6. **Coverage**: Cobertura de código (⚠️ **depende de Unit**)
7. **Performance**: Pruebas de carga con JMeter (requiere Flask)

### Restricciones Importantes

- 🔴 **Unit solo puede ejecutarse 1 vez** en todo el pipeline
- 🔴 **Coverage depende de los datos de Unit** (no puede ejecutarse independientemente)
- 🟡 **Rest y Performance** ambos requieren Flask corriendo

### Opción A: Máxima Paralelización (RECOMENDADA)

```
┌──────────────────────────────────────────────────────────┐
│ Get Code (Master/Any)                                    │
│ - git clone                                              │
│ - stash 'code'                                           │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ Tests Paralelos (3 stages en paralelo)                  │
├──────────────────┬─────────────────┬─────────────────────┤
│ Unit + Coverage  │ Rest + Perf     │ Static + Security   │
│ (Agent1)         │ (Agent2)        │ (Master/Any)        │
├──────────────────┼─────────────────┼─────────────────────┤
│ unstash 'code'   │ unstash 'code'  │ unstash 'code'      │
│                  │                 │                     │
│ 1. Ejecutar Unit │ 1. start Flask  │ 1. flake8 análisis  │
│    con coverage: │    start Mock   │    - threshold: 8   │
│    coverage run  │    pytest rest  │    - threshold: 10  │
│    -m pytest     │    junit report │                     │
│                  │                 │ 2. bandit análisis  │
│ 2. Generar XML:  │ 2. JMeter test  │    - threshold: 2   │
│    coverage xml  │    (reutiliza   │    - threshold: 4   │
│    coverage rpt  │     Flask)      │                     │
│                  │    perf report  │ publishIssues       │
│ 3. Publicar:     │                 │ (warnings-ng)       │
│    junit         │ 3. stop Flask   │                     │
│    publishCov    │    stop Mock    │                     │
│                  │                 │                     │
│ stash 'coverage' │                 │                     │
└──────────────────┴─────────────────┴─────────────────────┘
```

#### Ventajas de la Opción A

1. ✅ **Máxima paralelización**: 3 stages ejecutándose simultáneamente
2. ✅ **Optimización de tiempo**: El pipeline termina cuando termina el stage más lento
3. ✅ **Cumple restricción Unit**: Se ejecuta solo 1 vez, integrado con Coverage
4. ✅ **Reutilización de Flask**: Rest y Performance comparten la instancia de Flask, optimizando recursos
5. ✅ **Distribución inteligente de carga**:
   - Agent1: CPU-intensivo (Unit + Coverage)
   - Agent2: I/O-intensivo (Rest + Performance con servicios)
   - Master/Any: Ligero (análisis estático)
6. ✅ **Aprovecha los 3 nodos** disponibles eficientemente

#### Desventajas de la Opción A

- ⚠️ **Acoplamiento Rest-Performance**: Si Rest falla, Performance también falla (están en el mismo stage)
- ⚠️ **Mayor complejidad**: Requiere gestión cuidadosa de stash/unstash

### Opción B: Mayor Aislamiento

```
┌──────────────────────────────────────────────────────────┐
│ Get Code (Master/Any)                                    │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ Fase 1: Tests Paralelos                                 │
├──────────────────┬─────────────────┬─────────────────────┤
│ Unit + Coverage  │ Rest            │ Static + Security   │
│ (Agent1)         │ (Agent2)        │ (Master/Any)        │
└──────────────────┴─────────────────┴─────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ Fase 2: Performance                                      │
│ (Agent2)                                                 │
│ - start Flask                                            │
│ - JMeter tests                                           │
│ - stop Flask                                             │
└──────────────────────────────────────────────────────────┘
```

#### Ventajas de la Opción B

1. ✅ **Mayor aislamiento**: Si Rest falla, Performance puede ejecutarse
2. ✅ **Más fácil de debuguear**: Cada tipo de test es independiente
3. ✅ **Menos riesgo**: Fallos no se propagan entre Rest y Performance

#### Desventajas de la Opción B

1. ❌ **Tiempo total mayor**: Performance se ejecuta secuencialmente después de Fase 1
2. ❌ **Duplicación de esfuerzo**: Flask se levanta 2 veces (Rest y Performance)
3. ❌ **Menor eficiencia**: No aprovecha al máximo la paralelización

### Opción C: Dos Fases Paralelas

```
┌──────────────────────────────────────────────────────────┐
│ Get Code (Master/Any)                                    │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ Fase 1: Tests Ligeros y Coverage                        │
├──────────────────┬──────────────────────────────────────┤
│ Unit + Coverage  │ Static + Security                    │
│ (Agent1)         │ (Agent2 o Master)                    │
└──────────────────┴──────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│ Fase 2: Tests con Servicios                            │
├──────────────────┬──────────────────────────────────────┤
│ Rest             │ Performance                          │
│ (Agent1)         │ (Agent2)                             │
└──────────────────┴──────────────────────────────────────┘
```

#### Ventajas de la Opción C

1. ✅ **Buena paralelización**: 2 stages por fase
2. ✅ **Aislamiento Rest-Performance**: Se ejecutan independientemente
3. ✅ **Lógica clara**: Separa tests ligeros de tests pesados con servicios

#### Desventajas de la Opción C

1. ❌ **Tiempo total mayor**: 2 fases secuenciales
2. ❌ **No optimiza Flask**: Se levanta 2 veces
3. ❌ **Paralelización subóptima**: Solo 2 threads por fase en lugar de 3

---

## Comparación de Opciones

| Criterio                    | Opción A | Opción B | Opción C |
|-----------------------------|----------|----------|----------|
| Tiempo total                | ⭐⭐⭐    | ⭐       | ⭐⭐     |
| Paralelización              | ⭐⭐⭐    | ⭐⭐     | ⭐⭐     |
| Uso de recursos             | ⭐⭐⭐    | ⭐⭐     | ⭐⭐     |
| Aislamiento tests           | ⭐       | ⭐⭐⭐   | ⭐⭐⭐   |
| Facilidad debug             | ⭐⭐     | ⭐⭐⭐   | ⭐⭐⭐   |
| Optimización Flask          | ⭐⭐⭐    | ⭐       | ⭐       |
| Complejidad implementación  | ⭐⭐     | ⭐⭐     | ⭐⭐⭐   |

---

## Recomendación Final

### Para CP 1.2: **Opción A - Máxima Paralelización**

**Justificación:**

Se recomienda la **Opción A** por las siguientes razones prioritarias:

1. **Eficiencia de tiempo**: En un entorno de CI/CD, el tiempo total del pipeline es crítico. La Opción A minimiza este tiempo al ejecutar 3 stages en paralelo.

2. **Optimización de recursos**: Aprovecha inteligentemente los 3 nodos disponibles:
   - **Agent1** maneja trabajo CPU-intensivo (Unit + Coverage)
   - **Agent2** maneja trabajo I/O-intensivo con servicios (Rest + Performance)
   - **Master/Any** maneja análisis ligero (Static + Security)

3. **Cumplimiento de restricciones**: Unit se ejecuta exactamente 1 vez, integrado con Coverage de forma natural.

4. **Reutilización de servicios**: Flask se levanta 1 vez y sirve tanto para Rest como para Performance, evitando overhead.

5. **Escalabilidad**: Si en el futuro se añaden más agentes, el diseño permite fácilmente separar Rest y Performance.

**Justificación técnica del acoplamiento Rest-Performance:**

El acoplamiento de Rest y Performance en el mismo stage es **aceptable** porque:

- ✅ Ambos tests validan el mismo servicio (Flask API)
- ✅ Si Rest falla (API rota), Performance daría resultados inválidos de todos modos
- ✅ La optimización de tiempo compensa el riesgo de acoplamiento
- ✅ En entornos reales, es común ejecutar performance tests solo si los integration tests pasan

**Alternativa para mayor robustez:**

Si se requiere mayor aislamiento, la **Opción B** sería la segunda mejor opción, sacrificando ~20-30% de tiempo a cambio de mayor resiliencia ante fallos.

---

## Implementación de la Opción A

### Pseudocódigo del Jenkinsfile

```groovy
pipeline {
    agent none

    options {
        skipDefaultCheckout()
    }

    stages {
        stage('Get Code') {
            agent any
            steps {
                git 'https://github.com/nicolaujoan/helloworld.git'
                stash name:'code', includes:'**'
            }
        }

        stage('Tests Paralelos') {
            parallel {

                stage('Unit + Coverage') {
                    agent {label 'agent1'}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            unstash name:'code'
                            sh '''
                                whoami
                                hostname
                                echo "WORKSPACE: ${WORKSPACE}"

                                cd "${WORKSPACE}"
                                export PYTHONPATH="${WORKSPACE}"

                                # Ejecutar Unit con Coverage
                                python3 -m coverage run -m pytest --junitxml=result-unit.xml test/unit

                                # Generar reportes de Coverage
                                python3 -m coverage xml -o coverage.xml
                                python3 -m coverage report
                            '''

                            // Publicar resultados Unit
                            junit 'result-unit.xml'

                            // Publicar Coverage con thresholds
                            publishCoverage adapters: [coberturaAdapter('coverage.xml')],
                                sourceFileResolver: sourceFiles('STORE_ALL_BUILD'),
                                thresholds: [
                                    [thresholdTarget: 'Line', unhealthyThreshold: 85.0, unstableThreshold: 95.0],
                                    [thresholdTarget: 'Conditional', unhealthyThreshold: 80.0, unstableThreshold: 90.0]
                                ]
                        }
                    }
                }

                stage('Rest + Performance') {
                    agent {label 'agent2'}
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            unstash name:'code'
                            sh '''
                                whoami
                                hostname
                                echo "WORKSPACE: ${WORKSPACE}"

                                cd "${WORKSPACE}"

                                # Limpiar servicios previos
                                ./stop_wiremock.sh || true
                                ./stop_flask.sh || true

                                # Levantar servicios
                                export FLASK_APP="${WORKSPACE}/app/api.py"
                                python3 -m flask run --port 5000 > flask.log 2>&1 &
                                ./start_wiremock.sh
                                sleep 10

                                # Ejecutar Rest tests
                                export PYTHONPATH="${WORKSPACE}"
                                python3 -m pytest --junitxml=result-rest.xml test/rest

                                # Publicar resultados Rest
                                junit 'result-rest.xml'

                                # Ejecutar Performance tests (Flask ya está corriendo)
                                jmeter -n -t test-plan.jmx -l results.jtl

                                # Limpiar servicios
                                ./stop_wiremock.sh
                                ./stop_flask.sh
                            '''

                            // Publicar resultados Performance
                            perfReport sourceDataFiles: 'results.jtl'
                        }
                    }
                }

                stage('Static + Security') {
                    agent any
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            unstash name:'code'
                            sh '''
                                whoami
                                hostname
                                echo "WORKSPACE: ${WORKSPACE}"

                                cd "${WORKSPACE}"

                                # Análisis estático
                                flake8 --exit-zero --format=pylint app > flake8.out

                                # Análisis de seguridad
                                bandit -r . -f json -o bandit.json || true
                            '''

                            // Publicar Static
                            recordIssues tools: [flake8(pattern: 'flake8.out')],
                                qualityGates: [
                                    [threshold: 8, type: 'TOTAL', unstable: true],
                                    [threshold: 10, type: 'TOTAL', unhealthy: true]
                                ]

                            // Publicar Security
                            recordIssues tools: [pyLint(pattern: 'bandit.json')],
                                qualityGates: [
                                    [threshold: 2, type: 'TOTAL', unstable: true],
                                    [threshold: 4, type: 'TOTAL', unhealthy: true]
                                ]
                        }
                    }
                }
            }
        }
    }
}
```

---

## Conclusiones

### CP 1.1
La distribución de Unit en agent1 y Rest en agent2 es **óptima** para los recursos disponibles, logrando máxima paralelización y aprovechamiento de recursos.

### CP 1.2
La **Opción A (Máxima Paralelización)** es la estrategia recomendada porque:

1. Minimiza el tiempo total del pipeline (crítico en CI/CD)
2. Aprovecha eficientemente los 3 nodos disponibles
3. Cumple todas las restricciones técnicas (Unit 1 sola vez, Coverage depende de Unit)
4. Optimiza recursos al reutilizar servicios (Flask)
5. Distribuye inteligentemente la carga según tipo de trabajo (CPU vs I/O)

El acoplamiento de Rest y Performance es un trade-off aceptable considerando los beneficios en tiempo y eficiencia de recursos.

---

**Documento creado para:** Caso Práctico 1 - Experto Universitario en DevOps & Cloud - UNIR
**Fecha:** 2025-12-20
**Autor:** Joan Nicolau
