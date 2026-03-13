# Clase 06: NLP con Atencion

Material base recomendado: [14_nlp_with_rnns_and_attention.ipynb](https://github.com/ageron/handson-mlp/blob/main/14_nlp_with_rnns_and_attention.ipynb)

## Que estudia esta clase

El salto desde modelado secuencial clasico hacia mecanismos que aprenden a focalizarse en partes relevantes del contexto.

## Por que existe esta clase

En NLP aparece un problema serio cuando comprimimos una secuencia larga en un unico vector fijo:

- se pierde informacion,
- el modelo debe resumir demasiado,
- el contexto lejano se degrada.

La atencion existe para resolver eso: en vez de depender de un resumen unico, el modelo aprende a mirar directamente las partes relevantes de la entrada.

## Parte teorica

### 1. Embeddings

La razon de ser de los embeddings es representar palabras o tokens en un espacio donde proximidad semantica tenga sentido operativo.

Sin embeddings, el modelo veria IDs discretos sin estructura.

### 2. Encoder-Decoder

Esta arquitectura existe para tareas donde:

- la entrada y la salida son secuencias,
- sus longitudes pueden variar,
- hace falta transformar una secuencia en otra.

Ejemplos: traduccion, resumen, generacion condicionada.

### 3. Mecanismo de atencion

La atencion responde una pregunta esencial:

> si estoy generando este token ahora, ¿que partes de la entrada deberia consultar?

Su razon de ser es relajar el cuello de botella del vector fijo y volver el contexto selectivo.

### 4. Interpretabilidad parcial

Los pesos de atencion no equivalen a causalidad, pero ofrecen una pista util sobre donde el modelo focaliza su capacidad en cada paso.

## Parte tecnica

El estudiante deberia poder:

- explicar por que un encoder-decoder simple sufre en secuencias largas,
- describir conceptualmente queries, keys y values sin formalismo innecesario,
- entender por que la atencion mejora traduccion, resumen y QA,
- conectar esta clase con el surgimiento de Transformers.

## Preguntas clave

- ¿Que pierde un modelo al resumir todo en un unico estado?
- ¿Por que la atencion mejora el uso del contexto?
- ¿Que diferencia hay entre "tener memoria" y "tener acceso selectivo a la memoria"?

## Errores comunes

- Pensar que atencion reemplaza completamente el resto de la arquitectura.
- Confundir embeddings con conocimiento completo del lenguaje.
- Creer que los mapas de atencion son explicaciones definitivas.

## Cierre esperado

Esta clase debe dejar una intuicion fuerte: la atencion no es una moda; es una solucion elegante a un problema estructural del modelado secuencial.
