class Planeta:
    def __init__(self,name="null",satellites=0,mass=0.0,volume=0.0,diameter=0,distance=0,type="null",visible=False):
        self.name=name
        self.satellites=satellites
        self.mass=mass
        self.volume=volume
        self.diameter=diameter
        self.distance=distance
        self.type=type
        self.visible=visible
        pass
    def __str__(self):
        return f"Nombre: {self.name}, Satélites: {self.satellites}, Masa: {self.mass} (trillones de toneladas), Volumen: {self.volume} (millones de kilómetros cúbicos), Diámetro: {self.diameter} km, Distancia media al Sol: {self.distance} UA's, Tipo de planeta: {self.type}, Visible a simple vista: {self.visible}"
    
    def density(self):
        density = round((self.mass*1000000000000000000000/(self.volume*1000000000000000)),1)
        return f"La densidad es {density} kg/m^3."
    
    def exterior(self):
        if self.distance > 3.4:
            return f"Exterior: {True}."
        else:
            return f"Exterior: {False}."
    
La_Tierra = Planeta("Tierra",1,6,1000,12750,1,"Planeta Rocoso",True)
Kepler_22B = Planeta("Kepler_22B",0,La_Tierra.mass*9,La_Tierra.volume*13.5,La_Tierra.diameter*2,40500000,"Exoplaneta",False)

print(La_Tierra)
print(La_Tierra.density())
print(La_Tierra.exterior())
print("")
print(Kepler_22B)
print(Kepler_22B.density())
print(Kepler_22B.exterior())
print("")