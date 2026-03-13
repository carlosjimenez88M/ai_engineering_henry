# Clase 07: Transformers y Chatbots

Material base recomendado: [15_transformers_for_nlp_and_chatbots.ipynb](https://github.com/ageron/handson-mlp/blob/main/15_transformers_for_nlp_and_chatbots.ipynb)

## Que estudia esta clase

La arquitectura Transformer como solucion escalable para modelar lenguaje y construir sistemas conversacionales modernos.

## Por que existe esta clase

RNNs y variantes fueron un avance importante, pero tenian limites claros:

- paralelizacion pobre,
- dificultad para modelar dependencias largas,
- entrenamiento costoso en secuencias extensas.

Transformers existen porque self-attention permite:

- procesar tokens en paralelo,
- modelar relaciones largas con mas eficiencia,
- escalar mejor con datos y compute.

## Parte teorica

### 1. Self-attention

La idea central es que cada token puede ponderar la relevancia de los demas tokens del contexto. La razon de ser:

- capturar dependencias cercanas y lejanas,
- evitar el cuello secuencial de RNNs,
- construir contexto dinamico por token.

### 2. Multi-head attention

No toda relacion contextual es del mismo tipo. Multiples heads permiten aprender distintos patrones:

- sintacticos,
- semanticos,
- posicionales,
- de correferencia.

### 3. Positional encoding

Como la atencion por si sola no conoce orden, hace falta inyectar informacion posicional. Si no, el modelo veria una bolsa de tokens.

### 4. Pretraining y fine-tuning

La razon de ser del pretraining es aprovechar grandes corpus para aprender representaciones generales. Luego el fine-tuning adapta esa base a tareas concretas con menos datos.

### 5. Chatbots y generacion

Un chatbot moderno no es solo "un Transformer que responde". Necesita:

- manejo de contexto,
- estrategia de decodificacion,
- control de longitud y temperatura,
- evaluacion de calidad y seguridad.

## Parte tecnica

El estudiante deberia poder:

- explicar por que Transformers desplazaron a muchas arquitecturas previas en NLP,
- distinguir encoder, decoder y encoder-decoder,
- conectar pretraining con downstream tasks,
- entender por que los chatbots requieren mas que una llamada de inferencia.

## Preguntas clave

- ¿Por que self-attention escala mejor que recurrencia para muchos casos?
- ¿Que se gana y que se pierde con contexto largo?
- ¿Por que los modelos generativos necesitan estrategias de decoding?
- ¿Por que un buen modelo base no garantiza un buen sistema conversacional?

## Errores comunes

- Reducir Transformers a "modelos grandes".
- Olvidar el costo cuadratico de la atencion clasica.
- Confundir rendimiento de benchmark con calidad de producto.
- Creer que un chatbot se evalua solo por fluidez.

## Cierre esperado

El estudiante deberia terminar entendiendo que los Transformers no importan por moda, sino porque reorganizaron la forma de modelar contexto, escalabilidad y generalizacion en NLP.
