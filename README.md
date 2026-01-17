# Repo para EU - DevOps&Cloud - UNIR

Este repositorio incluye un proyecto sencillo para demostrar los conceptos de pruebas unitarias, pruebas de servicio, uso de Wiremock y pruebas de rendimiento
El objetivo es que el alumno entienda estos conceptos, por lo que el código y la estructura del proyecto son especialmente sencillos.
Este proyecto sirve también como fuente de código para el pipeline de Jenkins.

pd: recordar a ejecutar los agents antes de lanzar pipelines ;)

### Ejercicios (CP 1.1)

#### JENKINS 1

- [x] Crear y ejecutar un pipeline simple, una sola etapa con un "echo"
- [x] Añadir un comando git para traer todo el código fuente del repositorio
- [x] Verificar que el código se ha descargado mediante el comando dir (o ls -la)
- [x] Verificar cual es el espacio de trabajo (echo $WORKSPACE)
- [x] Añadir etapa "Build" (que no hace nada realmente, python codigo interpretado)

#### JENKINS 2

- [x] Añadir etapa unit lanzando solo las pruebas unitarias
- [x] Añadir etapa service (secuencial) lanzando las pruebas de servicio (iniciar servidores flask y wiremock antes de llamar a pytest test/rest)
- [x] Convertir ambas etapas para que se ejecuten en paralelo (añadir una etapa posterior para conectar con junit)

#### JENKINS 3

- [x] Crear un pipeline donde se use un jenkinsfile de vuestro repositorio en github
- [ ] Activar polling en jenkins para que se ejecute el pipeline cuando haya cambios (cuidar cron para la frecuencia, hacer cualquier cambio en el código y ver que se ejecuta el pipeline, desactivar el polling)
- [ ] Crear item Jenkins de tipo "Multibranch pipeline", conectado con el repositorio (verificar que se pueden ejecutar los pipelines de cada rama y bloquear la capacidad de ejecución del pipeline para la rama develop)

#### Reto 1 - Pipeline CI (40%)

- [x] Crear cuenta en GitHub
- [x] Descargar código fuente original de https://github.com/anietounir/helloworld.git
- [x] Replicar en repositorio propio en GitHub
- [x] Ejecutar en línea de comandos todas las pruebas unitarias y de integración
- [x] Crear pipeline Jenkins con etapas: Get Code, Unit, Rest
- [x] Usar Jenkinsfile del repositorio GitHub
- [x] Configurar mapping de Wiremock (sqrt64.json)

#### Reto 2 - Distribución de agentes (30%)

- [x] Configurar 3 agentes Jenkins (agent1, agent2, y master)
- [x] Dar de alta agentes usando conexión TCP o SSH
- [x] Modificar pipeline para asignar etapas a agentes específicos
- [x] Implementar stash/unstash para compartir archivos entre agentes
- [x] Incluir comandos whoami, hostname, echo ${WORKSPACE} en cada etapa
- [x] Limpiar workspace al finalizar cada etapa
- [ ] Justificar distribución de agentes elegida

#### Reto 3 - Ampliar microservicios (15%)

- [ ] Crear rama "develop" desde master
- [ ] Generar microservicio "multiply" con dos parámetros
- [ ] Generar microservicio "divide" con dos parámetros (devolver HTTP 406 si divisor es 0)
- [ ] Añadir tests de integración para multiply y divide
- [ ] Modificar Jenkinsfile si es necesario

#### Reto 4 - Mejorar fiabilidad (15%)

- [ ] Identificar error en etapa "Test Rest" cuando se ejecutan tareas en paralelo
- [ ] Reproducir el problema
- [ ] Detectar la causa del error
- [ ] Implementar solución al problema
- [ ] Explicar cuál sería la mejor solución (aunque se implemente una más sencilla)


### Ejercicios (CP 1.2)

#### Reto 1 - Pipeline CI (60%)

**Instalación de herramientas:**
- [x] Instalar módulos Python: pytest, flask, flake8, bandit, coverage
- [x] Instalar plugins Jenkins: JUnit, GitHub, cobertura, warnings-ng, performance
- [x] Instalar JMeter (v5.5 o superior)

**Etapas del Pipeline:**
- [ ] Eliminar etapa "Build"
- [ ] Eliminar etapa "Results" (cada test publicará sus propios resultados)
- [ ] Mantener etapa "Get Code" (automática desde SCM)
- [ ] Mantener etapa "Unit" (sin baremo, siempre verde, ejecutar solo 1 vez)
- [ ] Mantener etapa "Rest" (sin baremo, siempre verde)

**Nueva etapa "Static" - Análisis de código estático (flake8):**
- [ ] Ejecutar flake8 sobre el código
- [ ] Si ≥8 hallazgos → unstable (amarillo/naranja)
- [ ] Si ≥10 hallazgos → unhealthy (rojo)
- [ ] Pipeline continúa independientemente del resultado
- [ ] Publicar resultados con plugin warnings-ng

**Nueva etapa "Security Test" - Análisis de seguridad (bandit):**
- [ ] Ejecutar bandit sobre el código
- [ ] Si ≥2 hallazgos → unstable (amarillo/naranja)
- [ ] Si ≥4 hallazgos → unhealthy (rojo)
- [ ] Pipeline continúa independientemente del resultado
- [ ] Publicar resultados con plugin warnings-ng

**Nueva etapa "Coverage" - Cobertura de código (coverage):**
- [ ] Ejecutar coverage sobre pruebas unitarias
- [ ] Cobertura por líneas: <85% rojo, 85-95% unstable, >95% verde
- [ ] Cobertura por ramas: <80% rojo, 80-90% unstable, >90% verde
- [ ] Pipeline continúa independientemente del resultado
- [ ] Publicar resultados con plugin cobertura
- [ ] Recordar: pruebas unitarias solo se ejecutan 1 vez en todo el pipeline

**Nueva etapa "Performance" - Pruebas de carga (JMeter):**
- [ ] Crear test-plan JMeter: 5 hilos, 40 llamadas a /add, 40 llamadas a /subtract
- [ ] Levantar Flask antes de ejecutar JMeter
- [ ] Ejecutar test-plan desde línea de comandos
- [ ] Publicar resultados con plugin performance
- [ ] Incluir en entregables: valor "línea 90" para microservicio suma + captura gráfica

#### Reto 2 - Distribución de agentes (25%)

- [ ] Elegir y justificar separación de agentes para el pipeline
- [ ] Paralelizar todas las pruebas posibles
- [ ] Si alguna prueba no se puede paralelizar, explicar por qué y proponer solución
- [ ] Actualizar JENKINSFILE_agentes con asignación de etapas a agentes
- [ ] Implementar stash/unstash para compartir archivos entre nodos
- [ ] Limpiar workspace al finalizar cada etapa
- [ ] Incluir comandos: whoami, hostname, echo ${WORKSPACE} en cada etapa
- [ ] Configurar executors entre 2-4, ejecutar pipeline y obtener log
- [ ] Configurar executors en 1, ejecutar pipeline, explicar comportamiento y adjuntar log

#### Reto 3 - Mejora de cobertura (15%)

- [ ] Crear rama "feature_fix_coverage" desde master
- [ ] Modificar tests en test/unit para lograr 100% cobertura (líneas y ramas)
- [ ] NO modificar código en carpeta "app"
- [ ] NO usar "pragma: no cover"
- [ ] Explicar cuál era el problema de cobertura
- [ ] Explicar cuál ha sido la solución implementada
- [ ] Adjuntar log mostrando cobertura 100%
- [ ] Adjuntar gráficas de evolución de cobertura (plugin cobertura)