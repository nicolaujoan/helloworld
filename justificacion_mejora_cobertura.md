# Justificación de la Mejora de Cobertura

## Contexto

Este documento describe el análisis y la solución implementada para lograr el 100% de cobertura de código (líneas y ramas) en los tests unitarios del proyecto HelloWorld.

---

## Análisis del Problema de Cobertura

### Estado Inicial

Antes de las modificaciones, el reporte de cobertura mostraba:

```
Name              Stmts   Miss Branch BrPart  Cover
---------------------------------------------------
app/__init__.py       0      0      0      0   100%
app/api.py           24     24      6      0     0%
app/calc.py          24      1      4      1    93%
app/util.py           7      0      2      0   100%
---------------------------------------------------
TOTAL                55     25     12      1    52%
```

### Problemas Identificados

#### 1. api.py - 0% de cobertura (24 líneas sin cubrir)

**Causa:** El módulo `api.py` contiene el código de la API Flask con los endpoints REST (`/`, `/calc/add/<op_1>/<op_2>`, `/calc/substract/<op_1>/<op_2>`). Este código no estaba siendo testeado por los tests unitarios porque:

- Los tests unitarios existentes (`calc_test.py`, `util_test.py`) solo probaban las clases y funciones de lógica de negocio
- El código de `api.py` requiere simular peticiones HTTP para ser ejecutado
- Este tipo de código típicamente se testea con tests de integración (REST), no unitarios

**Líneas sin cubrir:**
- Líneas 1-10: Imports y configuración de Flask
- Líneas 13-15: Función `hello()` - endpoint raíz
- Líneas 18-24: Función `add()` - endpoint de suma (incluyendo manejo de excepciones)
- Líneas 27-33: Función `substract()` - endpoint de resta (incluyendo manejo de excepciones)

#### 2. calc.py - 93% de cobertura (1 línea y 1 rama sin cubrir)

**Causa:** La función `divide()` tiene una condición para manejar la división por cero:

```python
def divide(self, x, y):
    self.check_types(x, y)
    if y == 0:  # <- Esta rama no estaba cubierta
        raise TypeError("Division by zero is not possible")
    return x / y
```

**Rama sin cubrir:** La rama `if y == 0` nunca se ejecutaba porque no existía ningún test que llamara a `divide()` con el divisor igual a cero.

---

## Solución Implementada

### Restricciones del Ejercicio

- ❌ NO modificar código en la carpeta `app/`
- ❌ NO usar `pragma: no cover`
- ✅ Solo modificar tests en `test/unit/`

### Cambios Realizados

#### 1. Nuevo archivo: `test/unit/api_test.py`

Se creó un nuevo archivo de tests para cubrir el módulo `api.py` utilizando el **test client de Flask**, que permite simular peticiones HTTP sin necesidad de levantar un servidor real.

```python
from app.api import api_application

class TestApi(unittest.TestCase):
    def setUp(self):
        self.client = api_application.test_client()
        api_application.config['TESTING'] = True
```

**Tests añadidos:**

| Test | Descripción | Cobertura |
|------|-------------|-----------|
| `test_hello_endpoint` | Verifica el endpoint raíz `/` | Líneas 13-15 |
| `test_add_endpoint_correct_result` | Suma de enteros positivos | Líneas 18-22 (rama OK) |
| `test_add_endpoint_with_negative_numbers` | Suma con números negativos | Líneas 18-22 |
| `test_add_endpoint_with_floats` | Suma de decimales | Líneas 18-22 |
| `test_add_endpoint_with_invalid_params` | Suma con parámetros inválidos | Líneas 23-24 (rama excepción) |
| `test_substract_endpoint_correct_result` | Resta de enteros | Líneas 27-31 (rama OK) |
| `test_substract_endpoint_with_negative_result` | Resta con resultado negativo | Líneas 27-31 |
| `test_substract_endpoint_with_floats` | Resta de decimales | Líneas 27-31 |
| `test_substract_endpoint_with_invalid_params` | Resta con parámetros inválidos | Líneas 32-33 (rama excepción) |

#### 2. Modificación: `test/unit/calc_test.py`

Se añadió un nuevo test para cubrir la rama de división por cero:

```python
def test_divide_method_fails_with_division_by_zero(self):
    self.assertRaises(TypeError, self.calc.divide, 2, 0)
    self.assertRaises(TypeError, self.calc.divide, -5, 0)
    self.assertRaises(TypeError, self.calc.divide, 0, 0)
```

**Cobertura añadida:** Línea 23-24 de `calc.py` (la rama `if y == 0`)

---

## Estado Final

Después de las modificaciones, el reporte de cobertura muestra:

```
Name              Stmts   Miss Branch BrPart  Cover
---------------------------------------------------
app/__init__.py       0      0      0      0   100%
app/api.py           24      0      6      0   100%
app/calc.py          24      0      4      0   100%
app/util.py           7      0      2      0   100%
---------------------------------------------------
TOTAL                55      0     12      0   100%
```

### Resumen de Mejoras

| Módulo | Antes | Después | Mejora |
|--------|-------|---------|--------|
| api.py | 0% | 100% | +100% |
| calc.py | 93% | 100% | +7% |
| util.py | 100% | 100% | - |
| **TOTAL** | **52%** | **100%** | **+48%** |

---

## Conclusiones

### Lecciones Aprendidas

1. **La cobertura de código de API requiere tests específicos**: El código Flask no se ejecuta automáticamente al importar el módulo. Es necesario utilizar el test client para simular peticiones HTTP.

2. **Todas las ramas de decisión deben testearse**: La rama de división por cero en `calc.py` era un caso obvio que debía testearse, tanto por cobertura como por validación del comportamiento correcto del código.

3. **Los tests unitarios y de integración son complementarios**: Aunque `api.py` también se testea en `test/rest/`, es válido y recomendable tener tests unitarios que prueben el código de forma aislada usando mocks o test clients.

### Técnicas Utilizadas

- **Flask Test Client**: Permite ejecutar endpoints Flask sin levantar un servidor HTTP real
- **assertRaises**: Para verificar que se lanzan excepciones esperadas en casos de error
- **Branch Coverage**: El flag `--branch` de coverage.py asegura que se miden todas las ramas de decisión

---

**Documento creado para:** Caso Práctico 1.2 - Reto 3 - Experto Universitario en DevOps & Cloud - UNIR
**Fecha:** 2025-01-17
**Autor:** Joan Nicolau
