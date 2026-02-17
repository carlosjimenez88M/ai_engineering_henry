### Bases de datos Vectoriales 


### Conceptos claves 

<details>
  <summary> Lenguaje en Forma Númerica </summary>

    
  * __Bag of Words__: Es un algoritmo que representa palabras en vectores dispersos que registran la presencia de una palabra

  * __Word2Vec__ Representación de la palabra desde su significado dentro de un contexto de algunas palabras vecinas 

    ![](https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/Skip-gram.svg/1280px-Skip-gram.svg.png)
  
  * __Transformers__: Capturan el significado de las palabras dentro de un contexto dado.
  
  * __Tokenización__: Convertir texto en entrada o piezas que son el Input de algun modelo 
  * Al reunir los tokens únicos de varios documentos, se crea un vocabulario, cuyo tamaño determina la dimensión de nuestras representaciones.
  * __Representación Vectorial__: Es la frecuencia de tokens que aparece en un input o documentación especifica

</details>


<details>
  <summary> Embeddings </summary>

  * __Bag of words__ tiene un problema , ignora el significado semántica de las palabras dentro de un texto.
  *  __Word2Vec__: Se acerco a la premisa de capturar el significado de los textos dentro de embeddings.
     
     * Para lograr caputrar la atención de las palabras y el sentido de las mismas toco moverse al mundo del deep learning  donde a través de nodos interconectados , se generan arquitecturas del modelo que permiten que este procesamiento matematico permite ajustar el lenguaje con base al texto.
  
  * Un embedding intenta capturar el significado representando las propiedades de una palabra a través de valores (normalmente entre -1 y 1).
    * Ejemplo de dimensiones: La palabra "Pizza" podría tener un puntaje bajo en propiedades como "Robots" o "Darwinismo", pero alto en "Cómida" e "Italia". 
 * Esto es la base de la Búsqueda Semántica en sistemas RAG. UN agente encontrará información no por coincidencia de palabras exactas, sino porque los vectores están "cerca". 
 * __Modelos de representación__ : Son los modelos que convierten los textos en valores númericos.
   * Token Embeddings: División minuscula de palabras
   * Word Embeddings: Promedio de tokens de una palabra
   * Document Embeddings: Oraciones o documentos representados en Embeddings.
</details>



<details>
  <summary> Cómo funciona la arquitectura transformer LLMS ? </summary>

  ![](https://media.geeksforgeeks.org/wp-content/uploads/20251210153206327851/transformers.webp)

 * __Word2Vec__: Genera embeddings estáticos, lo cual es un pecado , a la hora de trabajar con busqueda semántica.
 * RNN (Redes Neuronales Recurrentes): Introdujeron la capcidad de modelar secuencias :
   * Encoder : Codifica secuencias de entrada y busca representarla en un formato númerico, ejemplo (dos brujas vigilan dos relojes , cuál bruja vigila cuál reloj ?)
   * Decoder: Decodifica  la salida del paso anterior y genera una salida 
 * Recordemos que existen dos tipos de modelos en GenAI :
   * Masked Lenguage model  : Predice el token perdido en una secuencia de texto , ejemplo : Mi ___ es Carlos  -> Mi _nombre_ es Carlos
   * Autoregresive Language model: Predice el siguiente token en una secuencia de texto , ejemplo: Mi mascota es un ___ -> Mi mascota es un _Dinosaurio_
 * Context Embeddings: Se usa Rag ya que al condensar todo un documento en un único corpus o embedding se pierde información
 * Attention (2014) : Representa que entradas son más relevantes dentro de un texto y dado un momento.
 * __Self Attention__ : es un mécanismo que permite que cada palabra mire todas las demás para entender su importancia relativa.
   * El self Attention combina dos cosas, el scoring que tiene una palabra en representación de un contexto + la combinación del contexto.
   * __Attention Head__ : Calcula su propio conjunto de relevance scores , el modelo combina las "opiniones" de todos los cabezales para tener una comprensión profunda y multidimensional del texto.
  
 * Token CLS: La "Etiqueta", En modelos de representación (Encoders), se usa un token especial llamado CLS (Classification). Este token actúa como un resumen numérico de toda la entrada, por ejemplo Si quieres que tu agente clasifique si un correo es SPAM o no, el modelo analiza el token CLS para tomar la decisión.
 * Context Window : El límite de tokens incluye tanto lo que se le envías (instrucciones + documentos) como lo que el modelo está generando en ese momento. Si se pasas de este límite, el agente "olvida" el inicio de la conversación.
</details>

### Bibliografia para este curso

* [Intelligent AI Delegation](https://arxiv.org/pdf/2602.11865)
* [Hands-On Large Language Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models)
* [Hands-On Machine Learning with Scikit-Learnand PyTorch](https://github.com/ageron/handson-mlp)
* [AI Engineering](https://github.com/chiphuyen/aie-book)
* [Designing Machine Learning Systems: An Iterative Process for Production-Ready Applications ](https://stanford-cs329s.github.io/)
* [Linear Algebra and Optimization for Machine Learning](https://turan-edu.uz/media/books/2024/05/28/1660642748.pdf)
* [Attention Is All You Need](https://arxiv.org/pdf/1706.03762) 