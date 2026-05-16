class Wing:
    def __init__(self,a_weight,airfoil,ar,air,material):
        import os
        self.a_weight = a_weight #newton
        self.air = air
        self.material = material
        self.ar = ar #default initial aspect ratio
        self.airfoil = airfoil
        self.wl = 0.5*self.air.rho*self.air.vs**2*0.9*self.airfoil.cl_max #wing loading
        self.dimensions()
    def dimensions(self):
        import numpy as np
        self.s = self.a_weight/self.wl #surface area
        self.b = np.sqrt(self.s*self.ar) #span
        print("span")
        print(self.b)
        self.Cl = 2*self.a_weight/(self.air.rho*self.air.vc**2*self.s)
        self.c = self.b/self.ar #chord
        print("corde")
        print(self.c)
        print("ar")
        print(self.ar)
        self.la = self.airfoil.la_unit * self.c**2 #Lateral area
        self.cla = self.airfoil.cla_unit*self.c #X center of lateral area
        self.mass = (self.la*self.b)*(2*self.material.rho +5)
    def aspect_ratio(self):
        from . import aero_analysis as aa
        import os
        rho = self.air.rho
        mu = self.air.mu
        vc = self.air.vc
        c = self.c
        i_Re = rho*vc*c/mu
        i_polar = aa.airfoil_analysis(i_Re,self.airfoil.coordinates)
        i_Cl,i_k,i_Cdo,i_Cm = aa.wing_analysis(self.c,self.b,self.ar,i_polar[0],i_polar[1],i_polar[2],self.Cl)
        i_Cd = i_Cdo + i_k*i_Cl**2
        while(True):
            self.ar = self.ar+0.05
            self.dimensions()
            if(self.c<0.18):
                os.system("cls")
                print("corde < 0.18")
                self.ar = self.ar-0.05
                self.dimensions()
                break
            n_Re = rho*vc*self.c/mu
            n_polar = aa.airfoil_analysis(n_Re,self.airfoil.coordinates)
            n_Cl,n_k,n_Cdo,n_Cm = aa.wing_analysis(self.c,self.b,self.ar,n_polar[0],n_polar[1],n_polar[2],self.Cl)
            n_Cd = n_Cdo+n_k*n_Cl**2
            if(round(n_Cd,3)<=round(i_Cd,3)):
                i_Cd = n_Cd
            else:
                self.ar = self.ar-0.05
                self.dimensions()
                break