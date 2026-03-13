# Clase 02: PyTorch para Modelos Entrenables

Material base recomendado: [10_neural_nets_with_pytorch.ipynb](https://github.com/ageron/handson-mlp/blob/main/10_neural_nets_with_pytorch.ipynb)

## Que estudia esta clase

La traduccion de la teoria de redes neuronales a una implementacion reproducible en PyTorch.

## Por que existe esta clase

Entender redes neuronales sin poder implementarlas deja el conocimiento a mitad de camino. PyTorch importa porque convierte ideas abstractas en un pipeline entrenable:

- tensores para representar datos,
- modulos para definir arquitectura,
- optimizadores para actualizar pesos,
- autograd para derivar automaticamente,
- dataloaders para escalar el entrenamiento.

La razon de ser de PyTorch no es "hacer deep learning moderno", sino reducir la friccion entre matematicas, codigo y experimentacion.

## Parte teorica

### 1. Tensor como estructura base

Un tensor es la generalizacion de escalar, vector y matriz. En Deep Learning importa porque:

- todo dato se representa como tensor,
- los pesos tambien son tensores,
- las operaciones del modelo son algebra tensorial.

### 2. `nn.Module`

Existe para encapsular:

- parametros aprendibles,
- estructura del modelo,
- forward pass.

Sin una abstraccion como esta, los modelos serian codigo suelto dificil de mantener, inspeccionar y guardar.

### 3. Autograd

La razon de ser de `autograd` es eliminar el costo de derivar a mano redes grandes. Permite:

- construir un grafo computacional,
- calcular gradientes automaticamente,
- iterar rapido sobre arquitecturas.

### 4. Dataset y DataLoader

No aparecen por comodidad sino por necesidad operativa:

- cargar datos por batches,
- mezclar muestras,
- desacoplar lectura de datos del entrenamiento.

Un loop serio de entrenamiento necesita esta capa de infraestructura.

## Parte tecnica

Al cerrar la clase, un estudiante deberia poder:

- crear tensores y entender sus shapes,
- definir una red simple con `nn.Sequential` o una clase propia,
- ejecutar un ciclo `forward -> loss -> backward -> step`,
- explicar la diferencia entre `model.train()` y `model.eval()`.

## Flujo practico minimo

1. Preparar datos.
2. Convertirlos a tensores.
3. Definir el modelo.
4. Definir loss y optimizer.
5. Entrenar por epochs.
6. Medir en validacion.

## Preguntas clave

- ¿Que gana PyTorch frente a escribir todo con `numpy`?
- ¿Por que el batch training existe?
- ¿Que pasa si olvidamos `optimizer.zero_grad()`?
- ¿Por que separar entrenamiento y evaluacion?

## Errores comunes

- Confundir `shape` incorrecto con "el modelo no aprende".
- No separar train/validation.
- Mirar solo accuracy y no la loss.
- Hacer loops sin guardar metricas.

## Cierre esperado

El estudiante deberia salir de esta clase con una rutina de entrenamiento minima y legible. Si no puede escribir y explicar ese loop, todavia no tiene base para avanzar a redes mas profundas.
