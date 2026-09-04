Taller 05 - Graficos de los ejercicios 15 al 25

Contenido:
- taller_05_graficos_15_25.py: programa principal.
- visor_taller_05_15_25.html: visor interactivo para abrir en el navegador.
- requirements_taller_05.txt: dependencias, por si se quieren instalar manualmente.
- ejecutar_guardar_pedidos.bat: genera solo los graficos pedidos directamente en la consigna.
- ejecutar_guardar_todos.bat: genera todos los graficos de apoyo disponibles del 15 al 25.

Graficos pedidos directamente:
- Ejercicio 15: superficie z=2x^2+y^2, curvas de interseccion y rectas tangentes.
- Ejercicio 16: superficie 36z=4x^2+9y^2, curvas de interseccion y rectas tangentes.
- Ejercicio 19: superficies para estudiar continuidad y derivadas parciales en el origen.

Apoyos visuales incluidos:
- Ejercicio 17: potencial electrostatico y curvas de nivel.
- Ejercicio 18: funcion de produccion Cobb-Douglas.
- Ejercicio 21: superficie de la funcion usada para derivadas mixtas.
- Ejercicio 23: superficie implicita xz-ln(z)=x+y, parametrizada con z>0.
- Ejercicio 24: superficie implicita x+y+yz^3-2xz=0.
- Ejercicio 25: resistencia equivalente y sensibilidad frente a R1, R2 y R3.

Uso facil:
1. Abrir visor_taller_05_15_25.html para ver los graficos interactivos.
2. Abrir ejecutar_guardar_pedidos.bat para generar solo 15, 16 y 19 en PNG.
3. Abrir ejecutar_guardar_todos.bat para generar todos los apoyos visuales en PNG.
4. Los PNG se guardan en graficos_taller_05_15_25.

Nota del visor HTML:
El visor usa Plotly desde CDN. Si el navegador no tiene internet, usa el script Python.

Orientacion 3D:
Las vistas 3D usan la terna derecha de dibujo de la foto: z vertical hacia
arriba, y horizontal hacia la derecha y x en diagonal hacia abajo-izquierda.

Uso por consola:
python taller_05_graficos_15_25.py --pedidos --guardar
python taller_05_graficos_15_25.py --todos --guardar
python taller_05_graficos_15_25.py --ejercicio 15 16 19 --guardar
python taller_05_graficos_15_25.py --listar

Instalacion manual opcional:
python -m pip install -r requirements_taller_05.txt

Nota sobre el ejercicio 24:
Segun el PDF, la ecuacion es x+y+yz^3-2xz=0 y el punto dado es (1,1,1).
Con esa ecuacion, F(1,1,1)=1, por lo que el punto no pertenece a la superficie.
El grafico lo deja marcado en rojo para advertir el posible error de enunciado.
