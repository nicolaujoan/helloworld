# Análisis de Resultados de Rendimiento (JMeter)

## Configuración del Test

| Parámetro | Valor |
|-----------|-------|
| Número de hilos (usuarios concurrentes) | 5 |
| Loops por hilo | 8 |
| Total peticiones por endpoint | 40 (5 × 8) |
| Endpoint suma | `/calc/add/4/9` |
| Endpoint resta | `/calc/substract/4/9` |
| Host | localhost |
| Puerto | 5000 |

---

## Valor "Línea 90" para el Microservicio Suma

Como se observa en la captura anterior, el valor **Line 90.0(ms)** para el endpoint **Add method** es de **4 ms**.

Este valor indica que el **90% de las peticiones** al endpoint `/calc/add/4/9` se completaron en **4 milisegundos o menos**.

---

## Análisis de las Gráficas

### 1. Throughput (Requests Per Second)

- **Valor observado**: ~100 requests/segundo
- **Comportamiento**: Estable y constante a lo largo de múltiples builds (#15 a #19)
- **Conclusión**: El servidor Flask puede manejar cómodamente la carga de 5 usuarios concurrentes sin degradación del rendimiento

### 2. Tiempo de Respuesta

- **Tendencia**: Estable entre 1-2 ms de media
- **Evolución**: Se mantiene constante entre builds, sin picos anómalos
- **Conclusión**: El rendimiento es predecible y consistente

### 3. Porcentaje de Errores

- **Valor**: 0.0% en todos los builds
- **Conclusión**: La API es completamente estable bajo esta carga de trabajo

---

## Interpretación de Métricas

### Media vs Mediana

Observando los resultados de la tabla, la media (2 ms) y la mediana (3 ms) son muy próximas. Esto indica una distribución simétrica de tiempos de respuesta, sin outliers significativos.

### Percentiles (P90 y P95)

- **P90 (Line 90%)**: 4-5 ms → El 90% de las peticiones se completan en este tiempo o menos
- **P95 (Line 95%)**: 4-5 ms → El 95% de las peticiones se completan en este tiempo o menos

La cercanía entre P90 y P95 indica baja variabilidad en los tiempos de respuesta.

### Min vs Max

La diferencia entre el valor mínimo (0-1 ms) y máximo (5-16 ms) es aceptable. El valor máximo de 16 ms en Add method puede deberse a:
- Inicialización de la primera petición
- Garbage collection de Python
- Variabilidad normal del sistema operativo

---

## Conclusiones

### Rendimiento General

1. ✅ **Excelente tiempo de respuesta**: Media de 2 ms es muy rápida para una API REST
2. ✅ **Alta disponibilidad**: 0% de errores indica estabilidad total
3. ✅ **Throughput adecuado**: 100 req/s es suficiente para esta aplicación
4. ✅ **Consistencia**: Los tiempos se mantienen estables entre ejecuciones

### Capacidad del Sistema

Con 5 usuarios concurrentes haciendo 8 peticiones cada uno (40 totales por endpoint):
- El servidor responde sin problemas
- No hay degradación del rendimiento
- No hay errores de timeout o conexión

### Escalabilidad Potencial

Los tiempos de respuesta tan bajos (2-4 ms) sugieren que el sistema podría escalar a más usuarios concurrentes antes de ver degradación significativa.

---

## Resumen Ejecutivo

La API Flask del proyecto HelloWorld demuestra un rendimiento excelente bajo las condiciones de prueba establecidas:

- **Throughput**: ~100 req/s (Excelente)
- **Tiempo medio respuesta**: 2 ms (Excelente)
- **Percentil 90 (suma)**: 4 ms (Excelente)
- **Tasa de errores**: 0.0% (Perfecto)
- **Estabilidad entre builds**: Constante (Excelente)

**Conclusión final**: El sistema es capaz de manejar la carga de prueba con tiempos de respuesta muy bajos y sin errores.

---

**Documento creado para:** Caso Práctico 1.2 - Reto 1 - Experto Universitario en DevOps & Cloud - UNIR
**Fecha:** 2025-01-17
**Autor:** Joan Nicolau
