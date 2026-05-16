class Vtail:
    def __init__(self,material,ssm,lamda,ar,wing,htail,fuselage):
        import os
        import sympy as sp
        import numpy as np
        from sympy import symbols
        s = symbols("Sv")
        h = htail
        f = fuselage
        w = wing 
        x_cg = f.l_avant #X cg is wanted just under the aerodynamic center of the wing
        self.lv = htail.lh - 0.01 #vertical tail arm
        self.ar = ar #vertical tail aspect ratio
        self.lamda = lamda #vertical tail taper ratio
        target_xcla = self.lv*ssm+x_cg #target Xcla
        h.cla = x_cg + h.lh -0.25*h.c+h.cla # htail X cla (origin: fuselage nose)
        w.cla = f.l_avant -0.25*w.c+w.cla # wing X cla (origin: fuselage nose)
        eq = -target_xcla + ((x_cg+ self.lv + 0.25*2/3*sp.sqrt(s/ar)*(1+lamda+lamda**2)/(1+lamda)**2)*s + h.cla*h.la + f.cla*f.la + w.cla*w.la)/(f.la + w.la + h.la + s)
        self.s = float(sp.re(sp.solve(eq)[0])) # Vtail found lateral area to achieve the target SSM
        self.b = np.sqrt(ar*self.s)
        self.mass = 0.07*self.s/self.b *self.s *(2*material.rho+5)
        self.cr = 2*(self.s/self.b)/(1+self.lamda)
        self.ct = self.lamda*self.cr
        self.mac = 2/3*self.cr*(1+lamda+lamda**2)/(1+lamda)
        self.v = self.lv*self.s/(wing.b*wing.s)
        #print("Vtail mass, b,s,c")
        #print(self.mass,"\t",self.b,"\t",self.s,"\t",self.s/self.b)

        

        

