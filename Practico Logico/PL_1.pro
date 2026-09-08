% 3 a

color(Fruta, verde, inmadura) :- fruta(Fruta).

color(naranja, naranja, madura).
color(pomelo, amarillo, madura).
color(frutilla, rojo, madura).
color(avocado, verde-oscuro, madura).

fruta(naranja).
fruta(pomelo).
fruta(frutilla).
fruta(avocado).

% 3 b

perro(sultan).
perro(fideo).
perro(dago).

gato(mimu).
gato(kitty).
gato(ona).

amigo(X, Y) :- amigo(Y, X).

amigo(ona, fideo).
amigo(fideo, sultan).
amigo(kitty, ona).

% 3 c

fruta(manzana).
fruta(naranja).

comible(X) :- fruta(X).

% 3 d

bar(lucia).
bar(frodo).
contenta(lucia).

canta(lucia) :- bar(lucia), contenta(lucia).

% 5

padre(oscar, valentin).
padre(oscar, victoria).
madre(cecilia, valentin).
madre(cecilia, victoria).

hijo(H, P, M) :- padre(P, H), madre(M, H).

hermano(X, Y) :- hermano(Y, X).

hermano(valentin, victoria).

% 6

padre(bruce, damian).
padre(bruce, dick).
padre(bruce, jason).
padre(bruce, tim).
padre(bruce, cassandra).
madre(talia, damian).

hijo_a(H, P) :- padre(P, H).

primo(X, Y) :- primo(Y, X).

primo(bruce, kate).

esposo(X, Y) :- esposo(Y, X).

esposo(bruce, talia).

% 7

amigo_7(juan, ana).
amigo_7(ana, miguel).
amigo_7(luis, isabel).
amigo_7(miguel, ana).
amigo_7(laura, juan).
amigo_7(isabel, luis).

amigos_mutuos(X, Y) :-
    amigo_7(X, Y),
    amigo_7(Y, X).

sin_corresponder(X, Y) :-
    amigo_7(X, Y),
    \+ amigo_7(Y, X).

% 8
hombre(antonio). hombre(juan). hombre(luis).
hombre(rodrigo). hombre(ricardo).
mujer(isabel). mujer(ana). mujer(marta).
mujer(carmen). mujer(laura). mujer(alicia).

esposo(antonio, ana).
esposo(juan, carmen).
esposo(luis, isabel).
esposo(rodrigo, laura).
esposo(X, Y) :- esposo(Y, X).

padre(antonio, juan).   padre(antonio, rodrigo). padre(antonio, marta).
padre(luis, carmen).    padre(juan, ricardo).    padre(rodrigo, alicia).
madre(ana, juan).       madre(ana, rodrigo).     madre(ana, marta).
madre(isabel, carmen).  madre(carmen, ricardo).  madre(isabel, alicia).

hijo(H, P, M) :- padre(P, H), madre(M, H).

progenitor(P, H) :- padre(P, H).
progenitor(P, H) :- madre(P, H).

% a) Nietos
nieto(N, A) :- padre(A, X), padre(X, N).
nieto(N, A) :- padre(A, X), madre(X, N).
nieto(N, A) :- madre(A, X), padre(X, N).
nieto(N, A) :- madre(A, X), madre(X, N).

% b) Abuelos
abuelo(A, N) :- nieto(N, A).

% c) Hermanos
hermano_8(X, Y) :- X \= Y,
                   padre(P, X), padre(P, Y),
                   madre(M, X), madre(M, Y).

% d) Tíos
tio(T, S) :- hombre(T), padre(X, S), hermano_8(X, T).
tio(T, S) :- hombre(T), madre(X, S), hermano_8(X, T).

% e) Tías
tia(T, S) :- mujer(T), padre(X, S), hermano_8(X, T).
tia(T, S) :- mujer(T), madre(X, S), hermano_8(X, T).

% f) Primos
% primo(P, X) = P es primo de X

primo(P, X) :-
    hombre(P),
    progenitor(A, P),
    progenitor(B, X),
    hermano_8(A, B).

% g) Primas
% prima(P, X) = P es prima de X

prima(P, X) :-
    mujer(P),
    progenitor(A, P),
    progenitor(B, X),
    hermano_8(A, B).

% h) Suegros
suegro(X, Y) :- esposo(Y, H), padre(X, H).
suegro(X, Y) :- esposo(Y, H), madre(X, H).

% 9

encargado_de_tarea(miguel, admision).
encargado_de_tarea(miguel, control).
encargado_de_tarea(miguel, vigilancia).
encargado_de_tarea(ricardo, planificacion).
encargado_de_tarea(ricardo, asesoramiento).
encargado_de_tarea(alicia, direccion).
encargado_de_tarea(alicia, control).

% Solo Elon es el CEO
ceo(elon).   

% a) Dos personas comparten alguna tarea
comparten(X, Y) :- X \= Y,
                   encargado_de_tarea(X, T),
                   encargado_de_tarea(Y, T).   

% b) Si comparten, ninguna es CEO
ninguno_es_ceo(X, Y) :- comparten(X, Y),
                        \+ ceo(X),
                        \+ ceo(Y).   

comparten(X, Y) :- comparten(Y, X).

% 10

juega(hector, baloncesto).
juega(miguel, balonmano).
juega(miguel, rugby).
juega(alicia, tenis).
juega(alicia, baloncesto).
juega(alicia, ajedrez).

mismo(X, Y) :- juega(X, D), juega(Y, D).
mismo(X, Y) :- mismo(Y, X).

% 12 a

maximo(A, B) :- A>B.
maximo(B, A) :- B>A.

% 12 b

area_c(A, R) :- A is pi * (R^2).

% 12 c

perimetro_r(P, A, B) :- P is 2*A + 2*B.

% 12 d

volumen_e(V, R) :- V is (4/3) * pi * R^3.

% 12 e

volumen_c(V, R, H) :- V is (pi * (R^2) * H) / 3.

% 12 f

velocidad(V, V0, T, A) :- V is V0 + A * T.

% 12 g

modulo(M, X, Y, Z) :- M is sqrt((X^2)+(Y^2)+(Z^2)).