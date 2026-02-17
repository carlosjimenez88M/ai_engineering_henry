# 02 - Programacion Orientada a Objetos (OOP)

Meta: modelar problemas reales con clases bien definidas, responsabilidades claras y contratos mantenibles.

## Critica del estado inicial (y mejora aplicada)

Problema detectado:
- El orden era correcto, pero faltaba criterio explicito para decidir entre composicion, herencia y dataclass.
- Faltaba enlace mas fuerte con escenarios de AI/ML (servicios, clientes, orquestacion).

Mejora aplicada:
- Se aclaro la ruta y el objetivo de decision arquitectonica por tema.
- Se mantiene foco en diseno pragmatico, no OOP academica.

## Ruta sugerida

1. `01_conceptos_base.md`
2. `02_clases_y_objetos.md`
3. `03_encapsulamiento.md`
4. `04_herencia_y_polimorfismo.md`
5. `05_composicion.md`
6. `06_dataclasses.md`
7. `07_diseno_y_criterios.md`
8. `08_logging_en_clases.md`
9. `ejercicios_guided.md`

## Resultado de salida del modulo

Al terminar deberias poder:

- Diseñar clases con bajo acoplamiento y alta cohesion.
- Decidir cuando usar composicion en lugar de herencia.
- Usar dataclasses cuando la clase es principalmente datos.
- Instrumentar clases con logging estructurado para observabilidad.

## Aplicacion AI/ML

Este modulo prepara para:

- Wrappers de proveedores LLM.
- Clases de retriever/vector store.
- Orquestadores con estado y trazabilidad.
- Servicios de inferencia con contratos claros.
