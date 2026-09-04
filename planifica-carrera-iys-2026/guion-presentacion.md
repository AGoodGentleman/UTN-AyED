# Guion breve para la exposicion oral

## 1. Presentacion del problema

Nuestro trabajo parte del caso de Martin, un estudiante que termino primer nivel pero no en la situacion ideal del plan de estudios. Tiene Algoritmos y Estructuras de Datos no regularizada, Analisis Matematico I regular con final pendiente y Fisica I regular con final pendiente. El problema es decidir que puede cursar, que no puede cursar y que decisiones le convienen para no bloquear su avance futuro.

## 2. Funcionamiento de la aplicacion

La aplicacion permite cargar el estado de cada materia como aprobada, regular, no regularizada o no cursada. Con esa informacion compara automaticamente el estado del estudiante con las correlatividades del plan.

El sistema muestra el plan por niveles, marca materias habilitadas, bloqueadas, finales pendientes y materias que deben recursarse. Tambien permite seleccionar una materia pendiente para ver su impacto en niveles posteriores.

## 3. Informacion utilizada

Usamos como base las asignaturas obligatorias de Ingenieria en Sistemas de Informacion Plan 2023 y su regimen de correlatividades. La aplicacion distingue dos tipos de requisitos:

- Correlativa por cursada regular: alcanza con tener la materia regular o aprobada.
- Correlativa por final aprobado: exige tener la materia aprobada.

## 4. Resultado del caso Martin

Para el segundo nivel, Martin puede cursar Analisis Matematico II, Fisica II, Ingenieria y Sociedad, Ingles II y Sistemas Operativos.

No puede cursar Sintaxis y Semantica de los Lenguajes, Paradigmas de Programacion ni Analisis de Sistemas de Informacion porque falta regularizar Algoritmos y Estructuras de Datos.

## 5. Criterio de recomendacion

La recomendacion no busca solamente maximizar la cantidad de materias cursadas. Tambien considera que materias destraban mas caminos futuros.

Por eso proponemos una planificacion equilibrada: recursar Algoritmos, cursar materias habilitadas y preparar primero el final de Analisis Matematico I. Esta opcion mantiene avance, pero tambien reduce los bloqueos que podrian trasladarse a tercero, cuarto y quinto nivel.

## 6. Mejoras posibles

Si la aplicacion se implementara para todos los estudiantes, se podria agregar conexion con el sistema academico, historial real de cursadas, vencimiento de regularidades, horarios, turnos de examen, recomendaciones por carga horaria y simulacion de distintos escenarios por cuatrimestre.

## Cierre

La idea central es que un sistema de informacion convierte datos academicos aislados en informacion para decidir. No reemplaza al estudiante ni a la secretaria academica, pero ayuda a visualizar restricciones, comparar alternativas y planificar con fundamento.
