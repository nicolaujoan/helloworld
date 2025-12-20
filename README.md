# Repo para EU - DevOps&Cloud - UNIR

Este repositorio incluye un proyecto sencillo para demostrar los conceptos de pruebas unitarias, pruebas de servicio, uso de Wiremock y pruebas de rendimiento
El objetivo es que el alumno entienda estos conceptos, por lo que el código y la estructura del proyecto son especialmente sencillos.
Este proyecto sirve también como fuente de código para el pipeline de Jenkins.

Ejecutar pytest desde jenkins:

I don't see a Jenkinsfile yet. Here are the best approaches: Option 1: Call venv Python directly (no activation needed)
./venv/bin/python -m pytest
# or
./venv/bin/pytest
Option 2: Activate venv in Jenkins pipeline
source venv/bin/activate && pytest

### Ejercicios (CP 1.1)

#### JENKINS 1

- Crear y ejecutar un pipeline simple, una sola etapa con un "echo"

- Añadir un comando git para traer todo el código fuente del repositorio

- verificar que el código se ha descargado mediante el comando dir (o ls -la)

- verificar cual es el espacio de trabajo (echo $WORKSPACE)

- añadir etapa "Build" (que no hace nada realmente, python codigo interpretado)

#### JENKINS 2

- Añadir etapa unit lanzando solo las pruebas unitarias

- Añadir etapa service (sequencial) lanzando las pruebas de servicio (iniciar servidores flask y wiremock antes de llamar a pytest test/rest)

- Convertir ambas etapas para que se ejecuten en paralelo (añadir una etapa posterior para conectar con junit)

#### JENKINS 3 

- Crear un pipeline donde se use un jenkinsfile de vuestro repositorio en github

- Activar polling en jenkins para que se ejecute el pipeline cuando haya cambios (cuidad cron para la frecuencia, hacemos cualquier cambio en el código y vemos que se ejecuta el pipeline y desactivamos el polling)

- Crear item Jenkins de tipo "Multibranch pipeline", conectado con el repositorio (verificar que se pueden ejecutar los pipelines de cada rama y bloquear la capacidad de ejecucion del pipeline para la rama develop)



### Ejercicios (CP 1.2)