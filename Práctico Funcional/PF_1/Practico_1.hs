-- sumar
sumar :: Float -> Float -> Float
sumar a b = a + b

-- distancia
distancia :: Float -> Float -> Float -> Float -> Float
distancia a b c d = sqrt((c-a)^2 + (d-b)^2)

-- hip
hip :: Float -> Float -> Float
hip a b = sqrt(a^2 + b^2)

-- positive
positive :: Float -> Bool
positive a = if a > 0 then True else False

-- hundred
hundred :: Float -> Float
hundred a = if a < 100 then a*2 else a

-- bigger
bigger :: Float -> Float -> String
bigger a b =
    if a > b
        then show a
        else if b > a
            then show b
            else "Ninguno"

-- signo
signo :: Float -> Float
signo a =
    if a > 0
        then 1
        else if a < 0
            then (-1)
            else 0

-- factorial
factorial :: Int -> Int
factorial a = if a > 0 then a * factorial(a-1) else 1

-- fibonacci
fibonacci :: Int -> Int
fibonacci 0 = 0
fibonacci 1 = 1
fibonacci n = fibonacci (n-1) + fibonacci (n-2)

-- mult
mult :: Float -> Float -> Float
mult a b = 
    if b > 0 then a + mult a (b-1)
    else if b < 0 then -a + mult a (b+1)
    else 0

-- sumarUno
sumarUno :: Int -> Int
sumarUno n = n + 1

suma :: Int -> Int -> Int
suma a 0 = a
suma a b
    | b > 0 = suma (sumarUno a) (b - 1)
    | b < 0 = suma (-(sumarUno (-a))) (b + 1)

-- long
long :: [Float] -> Int
long [] = 0
long (x:xs) = 1 + long (xs)

-- sumarImpares
sumarImpares :: [Int] -> Int
sumarImpares [] = 0
sumarImpares (x:xs) = if x `mod` 2 == 1 then x + sumarImpares(xs) else sumarImpares(xs)

-- sumaLista
sumaLista :: [Float] -> Float
sumaLista [] = 0
sumaLista (x:xs) = x + sumaLista(xs)

-- inversor
inversor :: [Float] -> [Float]
inversor [] = []
inversor (x:xs) = inversor (xs) ++ [x]

-- ultimo
ultimo :: [Float] -> Float
ultimo [x] = x
ultimo (_:xs) = ultimo xs

ultimo_v2 :: [Float] -> Float
ultimo_v2 xs = head (reverse xs)

-- letter
letter :: [Char] -> Char -> Int
letter [] a = 0
letter (x:xs) a =
    if x == a
        then 1 + letter xs a
        else letter xs a

-- repetir
repetir :: Int -> Char -> String
repetir x a = if x == 0 then "" else [a] ++ repetir (x-1) a

-- primera
primera :: String -> String
primera [] = ""
primera (x:xs) = [x]

-- dupe
dupe :: [Float] -> [Float]
dupe [] = []
dupe (x:xs) = x : x : xs

-- en
en :: [Float] -> Float -> Bool
en [] a = False
en (x:xs) a = if x == a then True else en (xs) a