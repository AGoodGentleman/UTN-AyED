% Proyecto 1 - Terminal de omnibus
%
% Respuestas guia:
%
% 1. Hace falta llevar control de las localidades visitadas porque las
% conexiones son de ida y vuelta. Si no controlo eso, el programa podria
% quedarse yendo de san_rafael a mendoza y de mendoza a san_rafael sin parar,
% o repetir muchas veces la misma localidad dentro del mismo recorrido.
%
% 2. Un recorrido valido es cualquier camino que llega desde el origen hasta
% el destino sin repetir localidades. El recorrido optimo es uno de esos
% recorridos, pero elegido porque tiene menor distancia, menor tiempo o menor
% costo. En el codigo se nota la diferencia porque recorrido/3 solo busca
% caminos posibles, mientras que menor_distancia/6, menor_tiempo/6 y
% menor_costo/6 primero juntan los recorridos y despues comparan sus totales.
%
% 3. En mi base pasa con san_rafael y mendoza. El recorrido directo es mas
% corto en kilometros, pero tiene un recargo. El recorrido por salto_rosas es
% un poco mas largo, pero sale menos. En la vida real podria pasar por peajes,
% empresas distintas, temporada alta o porque un tramo corto tiene menos
% demanda y termina saliendo mas caro.
%
% 4. Cuando no hay recorrido posible, decidi que el predicado no_hay_recorrido/2
% sea verdadero. Los predicados que buscan recorridos o minimos fallan, porque
% no tienen ningun camino para devolver. Tambien deje consulta_recorrido/2 para
% mostrar un mensaje mas claro.
%
% Decision de diseño:
% Modele cada conexion una sola vez y despues hice tramo/5 para que se pueda
% viajar en ambos sentidos. Para evitar ciclos uso una lista de visitadas. Si
% hay empate entre recorridos minimos, me quedo con el primero que se genera,
% porque para este proyecto me interesa una respuesta simple y entendible.
% Si el origen y el destino son iguales, lo tomo como error de carga del usuario.

% localidad(Localidad).

localidad(san_rafael).
localidad(salto_rosas).
localidad(san_luis).
localidad(general_alvear).
localidad(malargue).
localidad(mendoza).
localidad(tunuyan).

% conexion(Origen, Destino, DistanciaKm, TiempoMin, ExtraCosto).
%
% El costo base sale de la idea:
% costo = (768000 + 400 * km) / 40
%
% Esto ya que 768000 son dos salarios minimos, 400 pesos sale cada km de nafta y 40 pasajeros es la mitad de un colectivo promedio.
%
% ExtraCosto permite representar peajes, temporada alta o descuentos.
% Tunuyan queda sin conexiones para tener un caso sin recorrido posible.

conexion(san_rafael, salto_rosas, 20, 12, 0).
conexion(san_rafael, san_luis, 275, 165, 0).
conexion(san_rafael, general_alvear, 85, 50, 0).
conexion(san_rafael, malargue, 190, 114, 0).
conexion(san_rafael, mendoza, 230, 138, 22000).
conexion(salto_rosas, mendoza, 230, 145, 0).
conexion(general_alvear, san_luis, 250, 150, 0).
conexion(general_alvear, malargue, 260, 170, 0).
conexion(malargue, mendoza, 325, 210, 0).

% Costo de un tramo segun la formula.

costo_tramo(Km, Extra, Costo) :-
    Costo is ((768000 + (400 * Km)) / 40) + Extra.

% tramo/5 hace que las conexiones se puedan recorrer en ambos sentidos.

tramo(Origen, Destino, Distancia, Tiempo, Costo) :-
    conexion(Origen, Destino, Distancia, Tiempo, Extra),
    costo_tramo(Distancia, Extra, Costo).

tramo(Origen, Destino, Distancia, Tiempo, Costo) :-
    conexion(Destino, Origen, Distancia, Tiempo, Extra),
    costo_tramo(Distancia, Extra, Costo).

% Conexion directa.

conectadas_directamente(Origen, Destino) :-
    tramo(Origen, Destino, _, _, _).

no_hay_recorrido_directo(Origen, Destino) :-
    localidad(Origen),
    localidad(Destino),
    Origen \= Destino,
    \+ conectadas_directamente(Origen, Destino).

% Conexion directa o indirecta.

conectadas(Origen, Destino) :-
    recorrido(Origen, Destino, _).

no_hay_recorrido(Origen, Destino) :-
    localidad(Origen),
    localidad(Destino),
    Origen \= Destino,
    \+ recorrido(Origen, Destino, _).

% recorrido(Origen, Destino, Camino).
% Camino queda como una lista de localidades, sin repetir localidades.

recorrido(Origen, Destino, Camino) :-
    localidad(Origen),
    localidad(Destino),
    Origen \= Destino,
    recorrer(Origen, Destino, [Origen], CaminoAlReves),
    reverse(CaminoAlReves, Camino).

recorrer(Destino, Destino, Camino, Camino).

recorrer(Actual, Destino, Visitadas, Camino) :-
    tramo(Actual, Siguiente, _, _, _),
    \+ member(Siguiente, Visitadas),
    recorrer(Siguiente, Destino, [Siguiente | Visitadas], Camino).

% totales_recorrido(Camino, DistanciaTotal, TiempoTotal, CostoTotal).

totales_recorrido([_], 0, 0, 0).

totales_recorrido([Origen, Destino | Resto], DistanciaTotal, TiempoTotal, CostoTotal) :-
    tramo(Origen, Destino, Distancia, Tiempo, Costo),
    totales_recorrido([Destino | Resto], DistanciaResto, TiempoResto, CostoResto),
    DistanciaTotal is Distancia + DistanciaResto,
    TiempoTotal is Tiempo + TiempoResto,
    CostoTotal is Costo + CostoResto.

% Armo una lista con todos los recorridos posibles y sus totales.

recorridos_con_totales(Origen, Destino, Lista) :-
    findall(
        datos(Camino, Distancia, Tiempo, Costo),
        (
            recorrido(Origen, Destino, Camino),
            totales_recorrido(Camino, Distancia, Tiempo, Costo)
        ),
        Lista
    ).

% Recorrido de menor distancia.

menor_distancia(Origen, Destino, Camino, Distancia, Tiempo, Costo) :-
    recorridos_con_totales(Origen, Destino, Lista),
    minimo_distancia(Lista, datos(Camino, Distancia, Tiempo, Costo)).

minimo_distancia([Dato], Dato).

minimo_distancia(
    [datos(Camino1, Distancia1, Tiempo1, Costo1), datos(_, Distancia2, _, _) | Resto],
    Mejor
) :-
    Distancia1 =< Distancia2,
    minimo_distancia([datos(Camino1, Distancia1, Tiempo1, Costo1) | Resto], Mejor).

minimo_distancia(
    [datos(_, Distancia1, _, _), datos(Camino2, Distancia2, Tiempo2, Costo2) | Resto],
    Mejor
) :-
    Distancia1 > Distancia2,
    minimo_distancia([datos(Camino2, Distancia2, Tiempo2, Costo2) | Resto], Mejor).

% Recorrido de menor tiempo.

menor_tiempo(Origen, Destino, Camino, Distancia, Tiempo, Costo) :-
    recorridos_con_totales(Origen, Destino, Lista),
    minimo_tiempo(Lista, datos(Camino, Distancia, Tiempo, Costo)).

minimo_tiempo([Dato], Dato).

minimo_tiempo(
    [datos(Camino1, Distancia1, Tiempo1, Costo1), datos(_, _, Tiempo2, _) | Resto],
    Mejor
) :-
    Tiempo1 =< Tiempo2,
    minimo_tiempo([datos(Camino1, Distancia1, Tiempo1, Costo1) | Resto], Mejor).

minimo_tiempo(
    [datos(_, _, Tiempo1, _), datos(Camino2, Distancia2, Tiempo2, Costo2) | Resto],
    Mejor
) :-
    Tiempo1 > Tiempo2,
    minimo_tiempo([datos(Camino2, Distancia2, Tiempo2, Costo2) | Resto], Mejor).

% Recorrido de menor costo.

menor_costo(Origen, Destino, Camino, Distancia, Tiempo, Costo) :-
    recorridos_con_totales(Origen, Destino, Lista),
    minimo_costo(Lista, datos(Camino, Distancia, Tiempo, Costo)).

minimo_costo([Dato], Dato).

minimo_costo(
    [datos(Camino1, Distancia1, Tiempo1, Costo1), datos(_, _, _, Costo2) | Resto],
    Mejor
) :-
    Costo1 =< Costo2,
    minimo_costo([datos(Camino1, Distancia1, Tiempo1, Costo1) | Resto], Mejor).

minimo_costo(
    [datos(_, _, _, Costo1), datos(Camino2, Distancia2, Tiempo2, Costo2) | Resto],
    Mejor
) :-
    Costo1 > Costo2,
    minimo_costo([datos(Camino2, Distancia2, Tiempo2, Costo2) | Resto], Mejor).

% Predicado con mensajes para probar los casos borde.

consulta_recorrido(Origen, Origen) :-
    localidad(Origen),
    write('Error: el destino no puede ser igual al origen.'), nl.

consulta_recorrido(Origen, Destino) :-
    Origen \= Destino,
    recorrido(Origen, Destino, Camino),
    write('Recorrido encontrado: '), write(Camino), nl.

consulta_recorrido(Origen, Destino) :-
    Origen \= Destino,
    no_hay_recorrido(Origen, Destino),
    write('No hay recorrido posible entre esas localidades.'), nl.

consulta_directo(Origen, Destino) :-
    conectadas_directamente(Origen, Destino),
    write('Hay recorrido directo.'), nl.

consulta_directo(Origen, Destino) :-
    no_hay_recorrido_directo(Origen, Destino),
    write('No hay recorrido directo, habria que buscar con escala.'), nl.

% Consultas de prueba:
%
% 1)
% ?- recorrido(san_rafael, mendoza, Camino).
% Camino = [san_rafael, mendoza] ;
% Camino = [san_rafael, salto_rosas, mendoza] ;
% ...
%
% 2)
% ?- totales_recorrido([san_rafael, salto_rosas, mendoza], D, T, C).
% D = 250,
% T = 157,
% C = 40900.
%
% 3) El mas corto y el mas barato no coinciden.
% ?- menor_distancia(san_rafael, mendoza, Camino, D, T, C).
% Camino = [san_rafael, mendoza],
% D = 230,
% T = 138,
% C = 43500.
%
% ?- menor_costo(san_rafael, mendoza, Camino, D, T, C).
% Camino = [san_rafael, salto_rosas, mendoza],
% D = 250,
% T = 157,
% C = 40900.
%
% 4) No hay recorrido posible.
% ?- no_hay_recorrido(san_rafael, tunuyan).
% true.
%
% ?- consulta_recorrido(san_rafael, tunuyan).
% No hay recorrido posible entre esas localidades.
% true.
%
% 5) Origen y destino iguales.
% ?- consulta_recorrido(san_rafael, san_rafael).
% Error: el destino no puede ser igual al origen.
% true.
%
% 6) No hay recorrido directo, pero si con escala.
% ?- no_hay_recorrido_directo(salto_rosas, malargue).
% true.
%
% ?- recorrido(salto_rosas, malargue, Camino).
% Camino = [salto_rosas, san_rafael, malargue] ;