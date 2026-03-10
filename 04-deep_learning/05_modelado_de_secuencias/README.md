# Clase 05: Modelado de Secuencias

Material base recomendado: [13_processing_sequences_using_rnns_and_cnns.ipynb](https://github.com/ageron/handson-mlp/blob/main/13_processing_sequences_using_rnns_and_cnns.ipynb)

## Que estudia esta clase

Como modelar datos donde el orden importa: texto, series temporales, audio, eventos y logs.

## Por que existe esta clase

Muchos datos no son bolsas de features independientes. En una secuencia importa:

- que paso antes,
- cuanto del pasado sigue siendo relevante,
- como cambian los patrones en el tiempo.

RNNs, LSTMs, GRUs y convoluciones temporales existen para incorporar esa estructura temporal en el modelo.

## Parte teorica

### 1. RNN clasica

La razon de ser de una RNN es reutilizar estado entre pasos temporales. Eso permite que la salida en el tiempo `t` dependa de informacion anterior.

Problema: entrenar secuencias largas puede ser inestable por gradientes que desaparecen o explotan.

### 2. LSTM y GRU

Existen porque una RNN simple olvida demasiado facil o no controla bien el flujo de informacion. Las compuertas permiten:

- decidir que recordar,
- que olvidar,
- que exponer a la salida.

### 3. Convoluciones temporales

No toda secuencia necesita memoria recurrente. Una CNN temporal puede detectar patrones locales eficientes en tiempo. Su razon de ser es capturar ventanas temporales con alta paralelizacion.

### 4. Longitud de contexto

Toda arquitectura secuencial impone una decision importante: cuanta historia vale la pena modelar. Mas contexto no siempre mejora; a veces solo agrega ruido y costo.

## Parte tecnica

El estudiante deberia poder:

- reconocer cuando una tarea es realmente secuencial,
- distinguir memoria de corto y largo plazo,
- justificar LSTM vs GRU vs CNN temporal,
- analizar si el cuello de botella es capacidad, datos o longitud de secuencia.

## Casos practicos tipicos

- prediccion de series temporales,
- clasificacion de secuencias,
- generacion paso a paso,
- deteccion de patrones en eventos ordenados.

## Errores comunes

- Forzar RNN donde una ventana fija alcanza.
- Confundir "mas memoria" con "mejor generalizacion".
- No recortar secuencias ni hacer padding de forma consistente.
- Ignorar el costo computacional de secuencias largas.

## Cierre esperado

El estudiante ya deberia poder pensar una tarea con la pregunta correcta: ¿el orden importa lo suficiente como para justificar una arquitectura secuencial?
