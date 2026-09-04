-- pares
pares :: [Int]
pares = [x | x <- [1..20], x `mod` 2 == 0]

-- cuadrados
cuadrados :: [Int]
cuadrados = [x^2 | x <- [1..10]]

-- divisibles
divisibles :: [Int]
divisibles = [x | x <- [1..100], x `mod` 3 == 0]

-- impares
impares :: [Int]
impares = [x | x <- [1..20], x `mod` 2 == 1]

-- cubos
cubos :: [Int]
cubos = [x^3 | x <- [1..10]]

-- cuadrados_list
cuadrados_list :: [Int] -> [Int]
cuadrados_list xs = [x^2 | x <- xs]

-- pares_v2
pares_v2 :: [Int]
pares_v2 = [x | x <- [1..50], x `mod` 2 == 0, x `mod` 4 /= 0]

-- multiples
multiples :: [Int]
multiples = [x | x <- [1..100], x `mod` 2 == 0, x `mod` 3 == 0, x `mod` 5 == 0]

--También podría hacerse:
--multiples = [x | x <- [1..100], x `mod` 30 == 0]

-- bigger_10
bigger_10 :: [Int] -> [Int]
bigger_10 xs = [x | x <- xs, x > 10]

-- impares_list
impares_list :: [Int] -> [Int]
impares_list xs = [x | x <- xs, x `mod` 2 == 1, x > 5]

-- pairs
pairs :: [(Int, Int)]
pairs = [(x,y) | x <- [1..20], y <- [1..20], x + y <= 20]

-- long
long :: [String] -> [Int]
long xs = [length x | x <- xs]

-- len
len :: [a] -> Int
len xs = sum [1 | _ <- xs]

-- vocals
vocals :: String -> [Char]
vocals texto = [x | x <- texto, x `elem` ['a','e','i','o','u']]

-- quitarMinusculas
quitarMinusculas :: String -> String
quitarMinusculas texto = [x | x <- texto, x `elem` ['A'..'Z']]

-- mizip
mizip :: [a] -> [b] -> [(a,b)]
mizip [] _ = []
mizip _ [] = []
mizip (x:xs) (y:ys) = (x,y) : mizip xs ys

-- doblarNumeros
doblarNumeros :: [Int] -> [Int]
doblarNumeros xs = map (\x -> x * 2) xs

-- negativos
negativos :: [Int] -> [Int]
negativos xs = filter (\x -> x < 0) xs

-- mayoriaEdad
mayoriaEdad :: [Int] -> [String]
mayoriaEdad xs = map (\x -> if x >= 18 then "Mayor" else "Menor") xs

-- inversa
inversa :: [String] -> [String]
inversa xs = map (\x -> reverse x) xs

-- filtrarPares
filtrarPares :: [Int] -> [Int]
filtrarPares xs = filter (\x -> x `mod` 2 == 0) xs

-- calcularCuadrados
calcularCuadrados :: [Int] -> [Int]
calcularCuadrados xs = map (\x -> x * x) xs

-- calcularPromedio
calcularPromedio :: [Float] -> Float
calcularPromedio [] = 0
calcularPromedio xs = sum xs / fromIntegral (length xs)

-- aplicarALista
aplicarALista :: (a -> b) -> [a] -> [b]
aplicarALista f [] = []
aplicarALista f (x:xs) = f x : aplicarALista f xs

-- transformar
transformar :: [Int] -> [Int]
transformar xs = map (\x -> x * 2 + 3) xs

-- quicksort
quicksort :: [Int] -> [Int]
quicksort [] = []
quicksort (x:xs) = quicksort (filter (\y -> y <= x) xs) ++ [x] ++ quicksort (filter (\y -> y > x) xs)

-- primeraFinal
primeraFinal :: String -> String
primeraFinal "" = ""
primeraFinal (x:xs) = xs ++ [x]