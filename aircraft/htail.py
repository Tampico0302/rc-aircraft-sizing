class Htail:
    def __init__(self,material,airfoil,vh,wing):
        import sympy as sp
        import numpy as np
        from sympy import symbols
        import os
        l = symbols("lh")
        self.v = vh #horizontal tail volume coefficient
        self.ar = wing.ar - 2.43 #horizontal tail aspect ratio
        eq = -2*wing.c*wing.s*self.v/l**2 + 0.313832*(2-0.75*sp.sqrt(wing.c*wing.s*self.v/(self.ar*l))/l)*(l+0.75*sp.sqrt(wing.c*wing.s*self.v/(self.ar*l)))
        #print("optimum arm")
        self.lh = float(sp.solve(eq)[0]) #horizontal tail optimum arm
        #print(self.lh)
        #os.system("pause")
        self.s =self.v*wing.c*wing.s/self.lh # horizontal tail surface area
        self.b = np.sqrt(self.ar*self.s) #horizontal tail span
        self.c = self.s/self.b #horizontal tail corde (ch)
        self.la = airfoil.la_unit * self.c**2 # horizontal tail Lateral area
        self.cla = airfoil.cla_unit*self.c # horizontal tail X center of lateral area (origin = leading edge Htail)
        self.mass = (self.la*self.b)*(2*material.rho+5)
    