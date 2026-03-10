# Clase 03: Entrenamiento de Redes Profundas

Material base recomendado: [11_training_deep_neural_networks.ipynb](https://github.com/ageron/handson-mlp/blob/main/11_training_deep_neural_networks.ipynb)

## Que estudia esta clase

Los mecanismos que vuelven entrenable a una red profunda en la practica.

## Por que existe esta clase

Porque pasar de una red pequena a una red profunda no es solo "agregar capas". Al crecer la profundidad aparecen problemas reales:

- gradientes que explotan o desaparecen,
- optimizacion inestable,
- sobreajuste,
- entrenamiento lento,
- sensibilidad a la inicializacion.

Esta clase existe para responder una pregunta critica: ¿por que una red correcta en papel puede fallar por completo al entrenar?

## Parte teorica

### 1. Inicializacion de pesos

No es un detalle cosmético. Si los pesos arrancan mal:

- las activaciones pueden saturarse,
- los gradientes pueden volverse inutiles,
- el entrenamiento puede estancarse desde el inicio.

La razon de ser de esquemas como Xavier o He es mantener la señal en rangos razonables a lo largo de muchas capas.

### 2. Normalizacion

`BatchNorm` y variantes existen para estabilizar distribuciones internas durante el entrenamiento. En terminos practicos:

- aceleran convergencia,
- reducen sensibilidad a inicializacion,
- permiten entrenar redes mas profundas.

### 3. Optimizadores

No todos los problemas responden igual a SGD puro. Por eso existen `Momentum`, `RMSProp`, `Adam`:

- `SGD`: referencia conceptual clara,
- `Momentum`: suaviza trayectorias ruidosas,
- `Adam`: adapta learning rates por parametro.

La razon de ser de los optimizadores adaptativos es mejorar la eficiencia del aprendizaje cuando el espacio de parametros es complejo.

### 4. Regularizacion

Una red profunda tiene mucha capacidad. Eso es potencia, pero tambien riesgo. `Dropout`, `L2`, data augmentation y early stopping existen para evitar que el modelo memorice en lugar de generalizar.

### 5. Learning rate

El learning rate es probablemente el hiperparametro mas importante del entrenamiento:

- demasiado alto: diverge,
- demasiado bajo: aprende lentisimo o parece no aprender.

Los schedules existen para administrar esa tension.

## Parte tecnica

Al terminar la clase, el estudiante deberia poder:

- reconocer sintomas de gradiente inestable,
- elegir una inicializacion razonable segun activacion,
- justificar un optimizador,
- leer curvas de train/validation sin conclusiones ingenuas.

## Checklist de diagnostico

Cuando una red profunda falla, revisar:

1. ¿Los datos tienen escala razonable?
2. ¿La loss baja en train?
3. ¿Validation diverge mientras train mejora?
4. ¿El learning rate es demasiado agresivo?
5. ¿La arquitectura es innecesariamente profunda para la tarea?

## Errores comunes

- Elegir `Adam` sin entender por que.
- Usar dropout en todos lados "por las dudas".
- Tratar overfitting con mas epochs.
- No registrar experimentos.

## Cierre esperado

El estudiante deberia poder defender una configuracion de entrenamiento. No alcanza con decir "funciono"; tiene que poder explicar por que esa configuracion era razonable para esa red y esa tarea.
