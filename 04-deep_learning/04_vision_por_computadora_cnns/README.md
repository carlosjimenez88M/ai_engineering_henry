# Clase 04: Vision por Computadora con CNNs

Material base recomendado: [12_deep_computer_vision_with_cnns.ipynb](https://github.com/ageron/handson-mlp/blob/main/12_deep_computer_vision_with_cnns.ipynb)

## Que estudia esta clase

Como las redes convolucionales resuelven el problema de trabajar con imagenes sin destruir su estructura espacial.

## Por que existe esta clase

Una imagen no es solo un vector largo de pixeles. Tiene:

- vecindad local,
- patrones repetidos,
- jerarquia visual,
- invariancia parcial a traslaciones.

Las CNNs existen porque una MLP sobre pixeles crudos:

- ignora esa estructura,
- usa demasiados parametros,
- generaliza peor en tareas visuales.

## Parte teorica

### 1. Convolucion

La idea central es compartir pesos sobre distintas regiones de la imagen. La razon de ser:

- detectar el mismo patron en distintas posiciones,
- reducir drasticamente la cantidad de parametros,
- explotar localidad espacial.

### 2. Feature maps

Cada filtro aprende una señal distinta:

- bordes,
- texturas,
- formas,
- partes de objetos.

La red construye una jerarquia: de patrones simples a conceptos visuales mas abstractos.

### 3. Pooling

Existe para resumir respuestas locales y ganar robustez frente a pequeñas variaciones espaciales. Su costo es perder algo de detalle fino.

### 4. Transfer learning

No siempre conviene entrenar desde cero. En vision, muchas representaciones tempranas son reutilizables. La razon de ser del transfer learning es ahorrar datos, tiempo y compute.

## Parte tecnica

El estudiante deberia poder:

- explicar por que una CNN es mas natural que una MLP para imagenes,
- interpretar que hace un kernel convolucional,
- distinguir entre convolucion, activacion y pooling,
- justificar el uso de fine-tuning o feature extraction.

## Preguntas clave

- ¿Por que compartir pesos ayuda?
- ¿Que gana una CNN en eficiencia y generalizacion?
- ¿Cuando conviene congelar capas preentrenadas?
- ¿Que problema resuelve data augmentation en vision?

## Actividades sugeridas

1. Tomar una imagen y pensar que patrones simples aparecen primero.
2. Comparar parametros de una MLP vs una CNN para la misma entrada.
3. Interpretar train/validation en clasificacion de imagenes.
4. Discutir cuando el dataset propio es demasiado chico para entrenar desde cero.

## Errores comunes

- Creer que una CNN "ve" como un humano.
- Fine-tuning completo sin datos suficientes.
- Ignorar el costo de memoria y tiempo de imagenes grandes.
- Evaluar solo accuracy sin mirar errores por clase.

## Cierre esperado

La salida correcta de esta clase no es solo saber usar una CNN, sino entender por que la estructura espacial de la imagen exige una arquitectura distinta.
