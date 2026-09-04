piesAmetros :: Float -> Float
piesAmetros x = x/3.28084
metrosApies :: Float -> Float
metrosApies x = x*3.28084
millasAKms :: Float -> Float
millasAKms x = x*1.609344
kmAMillas :: Float -> Float
kmAMillas x = x/1.609344
pulgadasACM :: Float -> Float
pulgadasACM x = x*2.54
cmApulgadas :: Float -> Float
cmApulgadas x = x/2.54
main :: IO ()
main = putStrLn "Programa de conversiones cargado"