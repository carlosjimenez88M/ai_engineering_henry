# Python Software Engineering (ejemplo concreto)

## Problema
Priorizar tickets de soporte con reglas de negocio claras y auditables.

## Por que este ejemplo es Software Engineering
- Comportamiento determinista: misma entrada, misma salida.
- Dominio modelado con tipos (`Ticket`) y reglas explicitadas en funciones.
- Test unitarios directos sobre reglas criticas.
- Sin dependencia de modelo probabilistico ni evaluacion semantica.

## Flujo
1. Cargar tickets (`sample_tickets.json`).
2. Calcular score con reglas de negocio.
3. Clasificar prioridad (`P0` a `P3`).
4. Ordenar cola y exportar `queue_report.json`.

## Ejecutar
- `make run-se`: genera cola priorizada.
- `make test-se`: valida reglas clave.
