class Material:
    def __init__(self,name):
        self.name = name
        self.rho()
    def rho(self):
        if self.name == "EPS30":
            self.rho = 30 #kg/m^3
        elif self.name == "EPS24":
            self.rho = 24 #kg/m^3