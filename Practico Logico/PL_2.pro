% 1 

factorial(0, 1).

factorial(N, F) :-
    N > 0,
    N1 is N - 1,
    factorial(N1, F1),
    F is N * F1.

% 2

fibonacci(0, 0).
fibonacci(1, 1).

fibonacci(N, F) :-
    N > 1,
    N1 is N - 1,
    N2 is N - 2,
    fibonacci(N1, F1),
    fibonacci(N2, F2),
    F is F1 + F2.

% 3

lector(nombre("Ana", "Garrido", "Aguirre"), mujer, 31).
lector(nombre("Marta", "Cantero", "Lasa"), mujer, 20).
lector(nombre("Rodrigo", "Duque", "Soto"), hombre, 30).
lector(nombre("Juan", "Perez", "Lopez"), hombre, 25).
lector(nombre("Lucia", "Fernandez", "Gomez"), mujer, 28).
lector(nombre("Carlos", "Martinez", "Diaz"), hombre, 40).
lector(nombre("Sofia", "Romero", "Torres"), mujer, 22).
lector(nombre("Pedro", "Garrido", "Suarez"), hombre, 35).
lector(nombre("Elena", "Perez", "Acosta"), mujer, 27).
lector(nombre("Miguel", "Fernandez", "Rojas"), hombre, 33).
lector(nombre("Ana", "Gomez", "Perez"), mujer, 24).

% Mismo nombre pero diferentes apellidos

mismo_nombre_distinto_apellido(
    nombre(Nombre, Apellido1, Apellido2),
    nombre(Nombre, Apellido3, Apellido4)
) :-
    lector(nombre(Nombre, Apellido1, Apellido2), _, _),
    lector(nombre(Nombre, Apellido3, Apellido4), _, _),
    (Apellido1 \= Apellido3 ; Apellido2 \= Apellido4).

% Consultas posibles:
%
% ?- lector(_, _, _).
% ?- lector(Nombre, Sexo, Edad).
% ?- lector(Nombre, mujer, Edad).
% ?- lector(Nombre, hombre, Edad).
% ?- mismo_nombre_distinto_apellido(X, Y).

% 4

prestado(
    libro("Misericordia", autor("Benito", "Perez", "Galdos")),
    persona("Almudena", "Alegria", "Sol")
).

prestado(
    libro("Marianela", autor("Benito", "Perez", "Galdos")),
    persona("Juan", "Lopez", "Diaz")
).

prestado(
    libro("El Aleph", autor("Jorge", "Luis", "Borges")),
    persona("Maria", "Gomez", "Perez")
).

prestado(
    libro("Ficciones", autor("Jorge", "Luis", "Borges")),
    persona("Carlos", "Diaz", "Lopez")
).

prestado(
    libro("Rayuela", autor("Julio", "Cortazar", "")),
    persona("Sofia", "Martinez", "Rojas")
).

prestado(
    libro("Cien Anos de Soledad", autor("Gabriel", "Garcia", "Marquez")),
    persona("Pedro", "Fernandez", "Suarez")
).

% Saber si una persona tiene un libro prestado

tiene_libro_prestado(Persona) :-
    prestado(_, Persona).

% Saber si un libro esta prestado

libro_prestado(Libro) :-
    prestado(Libro, _).

% Saber si alguien es escritor

escritor(Autor) :-
    prestado(libro(_, Autor), _).

% Saber si un escritor es leido

leido(Autor) :-
    prestado(libro(_, Autor), _).

% Un escritor es leido si alguno de sus libros esta prestado

es_leido(Autor) :-
    prestado(libro(_, Autor), _).

% Consultas posibles:
%
% ?- tiene_libro_prestado(persona("Maria", "Gomez", "Perez")).
%
% ?- libro_prestado(
%        libro("El Aleph", autor("Jorge", "Luis", "Borges"))
%    ).
%
% ?- escritor(X).
%
% ?- leido(autor("Jorge", "Luis", "Borges")).
%
% ?- leido(_).
%
% ?- es_leido(autor("Benito", "Perez", "Galdos")).

% 5

alumno(
    1001,
    nombre("Juan", "Perez"),
    [8, 7, 9, 6]
).

alumno(
    1002,
    nombre("Maria", "Gomez"),
    [10, 9, 8, 10]
).

alumno(
    1003,
    nombre("Carlos", "Lopez"),
    [6, 5, 7, 8]
).

alumno(
    1004,
    nombre("Lucia", "Fernandez"),
    [4, 6, 5, 7]
).

alumno(
    1005,
    nombre("Pedro", "Martinez"),
    [9, 8, 8, 9]
).

alumno(
    1006,
    nombre("Sofia", "Romero"),
    [7, 10, 9, 8]
).

% Promedio de un alumno

promedio(Nombre, Promedio) :-
    alumno(_, Nombre, [N1, N2, N3, N4]),
    Promedio is (N1 + N2 + N3 + N4) / 4.

% Consultas posibles:
%
% Como le fue a un alumno conociendo el nombre
%
% ?- alumno(_, nombre("Juan", "Perez"), Notas).
%
%
% Como le fue en el examen 1
%
% ?- alumno(_, nombre("Maria", "Gomez"), [Nota1, _, _, _]).
%
%
% Como se llama el alumno de determinado legajo
%
% ?- alumno(1004, Nombre, _).
%
%
% Promedio
%
% ?- promedio(nombre("Juan", "Perez"), P).

% 6

suma_lista([], 0).

suma_lista([Cabeza | Cola], Suma) :-
    suma_lista(Cola, SumaCola),
    Suma is Cabeza + SumaCola.

% Consultas posibles:
%
% ?- suma_lista([5, 8, 3, 2], X).
%
% X = 18.
%
%
% ?- suma_lista([10, 20, 30], X).
%
% X = 60.

% 7

cantidad_lista([], 0).

cantidad_lista([_ | Cola], Cantidad) :-
    cantidad_lista(Cola, CantidadCola),
    Cantidad is CantidadCola + 1.

% Consultas posibles:
%
% ?- cantidad_lista([a, b, c, d], X).
%
% X = 4.
%
%
% ?- cantidad_lista([10, 20, 30, 40, 50], X).
%
% X = 5.
%
%
% ?- cantidad_lista([], X).
%
% X = 0.