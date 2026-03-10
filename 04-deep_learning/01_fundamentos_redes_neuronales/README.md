# Clase 01: Fundamentos de Redes Neuronales

Material base recomendado: [09_artificial_neural_networks.ipynb](https://github.com/ageron/handson-mlp/blob/main/09_artificial_neural_networks.ipynb)

## Que estudia esta clase

El paso desde modelos lineales hacia redes neuronales multicapa. Aqui aparece la idea central de todo el modulo: una red profunda no es magia, es una composicion de funciones parametrizadas que aprende representaciones utiles.

## Por que existe esta clase

Porque antes de usar PyTorch o Transformers hay que entender el problema que las redes neuronales intentan resolver:

- un modelo lineal no puede separar patrones no lineales complejos,
- muchos problemas reales no viven en una unica frontera recta,
- necesitamos modelos capaces de aprender transformaciones intermedias.

En otras palabras: las redes neuronales existen porque en muchos dominios la representacion correcta de los datos no viene dada; se aprende.

## Parte teorica

### 1. El perceptron

Es la unidad conceptual minima:

- toma entradas,
- calcula una combinacion lineal,
- aplica una decision.

Sirve para entender clasificacion binaria simple, pero es limitado: solo resuelve problemas linealmente separables.

### 2. La necesidad de capas ocultas

Una capa oculta permite aprender transformaciones intermedias. La razon de ser de una red multicapa es dividir un problema dificil en varias transformaciones mas manejables:

- la primera capa detecta patrones simples,
- las capas intermedias combinan patrones,
- la salida toma una decision final.

### 3. Activaciones no lineales

Sin no linealidad, apilar capas lineales sigue dando una funcion lineal. Por eso existen activaciones como `ReLU`, `sigmoid` o `tanh`: introducen flexibilidad real.

La pregunta practica no es "que activacion suena mejor", sino:

- `sigmoid`: util en salida binaria, pero puede saturarse,
- `tanh`: centra mejor que sigmoid, pero tambien satura,
- `ReLU`: barata y efectiva para entrenamiento profundo, aunque puede dejar neuronas muertas.

### 4. Funcion de costo

La red necesita una forma cuantitativa de saber si va bien o mal. Esa es la razon de ser de la loss:

- mide el error,
- orienta la optimizacion,
- hace entrenable al modelo.

Sin una loss bien definida, no existe criterio claro de aprendizaje.

### 5. Backpropagation

No es una "caja negra matematica": es la forma eficiente de repartir la responsabilidad del error a cada peso de la red usando regla de la cadena.

La intuicion correcta es:

- la salida falla,
- ese error se propaga hacia atras,
- cada parametro recibe una señal sobre cuanto contribuyo al error.

## Parte tecnica

Al cerrar la clase, un estudiante deberia poder:

- describir una red feedforward en terminos de capas, pesos y activaciones,
- explicar por que una MLP modela no linealidad,
- distinguir entre inferencia y entrenamiento,
- justificar por que backprop es una necesidad computacional y no un detalle decorativo.

## Preguntas que esta clase debe responder

- ¿Por que una red neuronal puede resolver lo que una regresion lineal no?
- ¿Por que las activaciones importan tanto?
- ¿Que problema exacto resuelve backpropagation?
- ¿Que significa que una red "aprenda una representacion"?

## Actividades sugeridas

1. Dibujar una red simple con dos entradas, una capa oculta y una salida.
2. Identificar donde aparecen pesos, bias, activaciones y loss.
3. Comparar conceptualmente:
   - modelo lineal,
   - perceptron,
   - MLP de una capa oculta.
4. Explicar con tus palabras por que una pila de capas lineales no alcanza.

## Errores comunes

- Creer que "mas capas" siempre significa "mejor modelo".
- Pensar que backpropagation y descenso por gradiente son lo mismo.
- Usar lenguaje mistico: "la red entiende". Lo correcto es "la red ajusta parametros para minimizar una loss".

## Cierre esperado

Si esta clase salio bien, el estudiante ya no ve una red neuronal como una caja negra, sino como una cadena de decisiones matematicas con un objetivo claro: transformar entradas en representaciones cada vez mas utiles para una tarea.
