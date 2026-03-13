# Deep Learning

Modulo de estudio para aprender Deep Learning con criterio tecnico y una ruta reproducible en laptop comun. La propuesta esta pensada para clase real: teoria breve, notebooks ejecutables, ejemplos pequenos y validacion automatica.

## Objetivo del modulo

Al terminar este recorrido, una persona estudiante deberia poder:

- explicar por que una red neuronal supera a un modelo lineal en problemas no lineales,
- entrenar modelos en PyTorch con un pipeline reproducible,
- diagnosticar fallas comunes de entrenamiento,
- distinguir cuando conviene usar MLPs, CNNs, RNNs, atencion o Transformers,
- leer curvas, errores y tradeoffs sin tratar al modelo como caja negra.

## Filosofia de trabajo

- `CPU-first`: lo obligatorio debe correr en macOS, Linux y Windows sin GPU.
- `Offline-first`: la ruta validada no descarga datasets ni modelos despues de `uv sync`.
- `Teoria con razon de ser`: cada clase responde primero "por que existe esto".
- `Practica con criterio`: no alcanza con entrenar; hay que interpretar.

## Instalacion rapida

```bash
cd 04-deep_learning
uv sync --extra dev
make doctor
make test
make corpus-check
make notebooks-smoke
```

Guia ampliada: [INSTALACION.md](./INSTALACION.md)

## Ruta de clases

| Orden | Clase | Notebook principal | Enfoque |
|---|---|---|---|
| 01 | Fundamentos de redes neuronales | `01_fundamentos_redes_neuronales/01_anns_desde_cero.ipynb` | perceptron, MLP, activaciones, backprop |
| 02 | PyTorch para entrenamiento | `02_pytorch_fundamentos/01_pytorch_pipeline_entrenamiento.ipynb` | tensores, `Dataset`, `DataLoader`, train loop |
| 03 | Entrenamiento profundo | `03_entrenamiento_redes_profundas/01_estabilidad_y_regularizacion.ipynb` | inicializacion, normalizacion, regularizacion |
| 04 | Vision por computadora | `04_vision_por_computadora_cnns/01_cnns_y_reconocimiento_visual.ipynb` | CNNs, pooling, receptive field, comparaciones |
| 05 | Modelado de secuencias | `05_modelado_de_secuencias/01_rnns_lstm_gru_y_cnns_temporales.ipynb` | RNN, LSTM, GRU, CNN temporal, padding |
| 06 | NLP con atencion | `06_nlp_con_atencion/01_nlp_con_atencion_las_mil_y_una_noches.ipynb` | embeddings, ventanas de texto, atencion |
| 07 | Transformers y chat local | `07_transformers_y_chatbots/01_transformers_y_chat_local.ipynb` | positional embeddings, mascara causal, decoding |

## Que incluye el modulo

- 7 notebooks en espanol, una por clase, listas para ejecutar con `nbclient`
- corpus local de `Las mil y una noches` para NLP y Transformers
- utilidades compartidas en `tools/`
- tests de integridad, corpus y runner
- comandos `make` para instalar, validar y correr notebooks

## Ruta validada y ruta opcional

La ruta validada es completamente offline y CPU-first. Eso significa:

- no depende de `download=True`,
- no depende de credenciales,
- no depende de GPU,
- no depende de celdas de Colab.

Ademas hay celdas opcionales protegidas por `HENRY_DL_ONLINE_MODE=1` para probar un modelo pequeno descargable y comparar la diferencia entre un modelo entrenado en clase y un modelo preentrenado moderno.

## Validacion del modulo

`make test` valida:

- imports minimos de PyTorch, torchvision y Transformers,
- presencia del corpus local,
- existencia de notebooks, runner y rutas esperadas,
- funciones de chunking y utilidades del corpus.

`make notebooks-smoke` ejecuta las 7 notebooks con `HENRY_DL_SMOKE=1` para confirmar que cierran end-to-end en modo reducido.

## Requisitos previos

- Python intermedio
- algebra lineal basica
- nocion de derivadas y optimizacion
- experiencia inicial con `numpy`, `matplotlib` y lectura de codigo Python

## Regla de estudio recomendada

1. Leer el `README.md` de la clase.
2. Abrir la notebook y entender la celda de configuracion.
3. Identificar el problema que la arquitectura intenta resolver.
4. Ejecutar el ejemplo completo.
5. Revisar las curvas y responder los ejercicios.
6. Repetir solo despues de entender el cierre de la clase.
