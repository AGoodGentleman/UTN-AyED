class Triangulo:
    def __init__(self,L1,L2,L3):
        self.L1 = L1
        self.L2 = L2
        self.L3 = L3
        self.s = ((L1 + L2 + L3)/2)

    def area(self):
        return f"El área del triángulo es {self.s * (self.s - self.L1) * (self.s - self.L2) * (self.s - self.L3)}."
    
    def perimeter(self):
        return f"El perímetro del triángulo es {self.L1 + self.L2 + self.L3}."
    
    def form(self):
        if self.L1 == self.L2 == self.L3:
            return "El triángulo es equilátero."
        elif self.L1 == self.L2 or self.L1 == self.L3 or self.L2 == self.L3:
            return "El triángulo es isóceles."
        else:
            return "El triángulo es escaleno."
    
    def __str__(self):
        return f"Lados: {self.L1},{self.L2},{self.L3}."
        
triangle_1 = Triangulo(3,4,5)

triangle_2 = Triangulo(5,5,10)

triangle_3 = Triangulo(3,3,3)

print("Triángulo 1: ")
print(triangle_1)
print(f"{triangle_1.area()}")
print(f"{triangle_1.perimeter()}")
print(f"{triangle_1.form()}")

print("Triángulo 2: ")
print(triangle_2)
print(f"{triangle_2.area()}")
print(f"{triangle_2.perimeter()}")
print(f"{triangle_2.form()}")

print("Triángulo 3: ")
print(triangle_3)
print(f"{triangle_3.area()}")
print(f"{triangle_3.perimeter()}")
print(f"{triangle_3.form()}")