class Fuselage:
    
    def __init__(self):
        self.d_l = 1 #m
        self.d_cla = 0.41424 #m
        self.d_la = 0.074052  #m^2
        self.d_volume =  0.00435 #m^3        
    def dimensions(self,wing,htail,l_avant,material):
        import os
        self.l_avant = l_avant*wing.c #distance LE fuselga -- aerodynamic center wing
        self.l_arriere = htail.lh+3/4*htail.c
        self.l = self.l_avant+ self.l_arriere #fuselage length
        self.la= self.d_la*self.l**2 #fuselage lateral area
        self.cla = self.d_cla*self.l #fuselage  X center of lateral area
        self.mass = self.d_volume*self.l**3* (2*material.rho + 5)
        #print("fuselage dimensions: lavant, l,  mass")
        #print(self.l_avant,"\t",self.l,"\t",self.mass)
        #os.system("pause")
    
        


    

