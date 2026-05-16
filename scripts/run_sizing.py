from imaplib import IMAP4_SSL
from aircraft.wing import Wing
from aircraft.htail import Htail
from aircraft.vtail import Vtail
from aircraft.fuselage import Fuselage
from aircraft.material import Material
from aircraft.air import Air
from aircraft.airfoil import Airfoil
import numpy as np
from scipy import optimize

i_mass = 1.246 #kg #initial mass
i_ar = 5.53 #initial wing aspect ratio
vh = 0.6 #htail volume
i_ssm = 0.33 # initial static stability margin
lamda_v  = 0.63 # V. Tail taper ratio
ar_v = 1.6 # V. Tail aspect ratio
w_material = Material("EPS30") #wing (and H. Tail, V. Tail) material
f_material = Material("EPS24") #fuselage material
air = Air(1.1596,13,7,0.00001858) #air parameters (density,cruise speed, stall speed, dynamic viscosity)
w_airfoil = Airfoil("ishii") #wing airfoil
h_airfoil = Airfoil("naca0007") #Ht. Tail airfoil
def f(in_mass):
    a_weight = in_mass*9.81 #aircraft weight
    wing = Wing(a_weight,w_airfoil,i_ar,air,w_material) #wing instance
    wing.aspect_ratio() #algorithme of the figure x.x (aspect ratio determination)
    htail = Htail(w_material,h_airfoil,vh,wing) #H. tail instance
    fuselage = Fuselage() # fuselage instance
    fuselage.dimensions(wing,htail,1.635,f_material) #dimensions calculation of fuselage (length, width,height)
    vtail = Vtail(w_material,i_ssm,lamda_v,ar_v,wing,htail,fuselage) #Vtail instance
    out_mass = 0.346+wing.mass+htail.mass+fuselage.mass+vtail.mass#final mass(electronic mass(0.346kg)+components mass)
    os.system("cls")
    print("\n--- Iteration ---")
    print(f"Input mass: {in_mass:.3f} kg")
    print(f"Output mass: {out_mass:.3f} kg")
    print(f"Wing aspect ratio: {wing.ar:.3f}")
    print("fuselage: lavant, larriere, ltotale masse")
    print(fuselage.l_avant,"\t",fuselage.l_arriere,"\t",fuselage.l,"\t",fuselage.mass)
    print("wing: S, b, c, ar, ws, mass")
    print(wing.s,"\t",wing.b,"\t",wing.c,"\t",wing.ar,"\t",wing.wl,"\t",wing.mass)
    print("Htail: S, b, c, mass")
    print(htail.s,"\t",htail.b,"\t",htail.c,"\t",htail.mass)
    print("Vtail: S, b, cr, ct, mac, lv,Vv, mass")
    print(vtail.s,"\t",vtail.b,"\t",vtail.cr,"\t",vtail.ct,"\t",vtail.mac,"\t",vtail.lv,"\t",vtail.v,"\t",vtail.mass)    

    return out_mass - in_mass
final_mass = optimize.newton(f,i_mass,tol=0.001)
print("final mass")   
print(final_mass)