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