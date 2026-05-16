from scipy.interpolate import CubicSpline
import numpy as np
import os

from .xfoil_runner import run_xfoil
from .polar_reader import read_xfoil_polar

def airfoil_analysis(Re, coordinates):
    polar_file = run_xfoil(
        coordinates=coordinates,
        reynolds=Re,
        mach=0.0,
        alpha_start=-3.0,
        alpha_end=15.0,
        alpha_step=0.25,
    )

    polar = read_xfoil_polar(polar_file)

    a = polar["alpha"]
    cl = polar["cl"]
    cd = polar["cd"]
    cm = polar["cm"]

    max_cl_index = list(cl).index(max(cl))

    a = a[:max_cl_index + 1]
    cl = cl[:max_cl_index + 1]
    cd = cd[:max_cl_index + 1]
    cm = cm[:max_cl_index + 1]

    cs_cl = CubicSpline(a, cl)
    cs_cd = CubicSpline(a, cd)
    cs_cm = CubicSpline(a, cm)

    return cs_cl, cs_cd, cs_cm

def wing_analysis(chord,span,AR,cs_cl,cs_cd,cs_cm,Cl):
    aoa =0
    r = 40  # spanwise divisions
    N = r-1
    # angular locations of the stations (except for y= +-span/2 (sin(0) = sin(pi)=0)
    theta_n = [i*np.pi/(r) for i in range(1, r)]
    yn = [round(-span/2 * np.cos(theta_n[i]), 4)
          for i in range(len(theta_n))]  # station positions
    yn[yn.index(-0.0)] = abs(yn[yn.index(-0.0)])
    # Normalizing
    etha_n = abs(np.array(yn)*2/span)
    etha_n = [round(etha_n[i], 3) for i in range(len(etha_n))]
    etha_m = [(np.pi/(2*r))*np.sin(theta_n[i]) for i in range(N)]
    zlaoa = list()
    lcslp = list()
    cordes = np.array([chord for i in range(N)])
    #default lift curve slope and zero lift angle of attack
    lcslp = [0.07 for i in range(N)]
    zlaoa = [-13 for i in range(N)]
    final_cl = list()
    c_aoa = list()
    A1 = Cl/(np.pi*AR)
    for iteration in range(100):
        if iteration == 99:
            raise("stop iteration max atteint (no convergence)")
        k = [chord*lcslp[i]/(4*span) for i in range(N)]
        LHS = [k[i]*np.sin(theta_n[i])*(-zlaoa[i]) - (Cl/(np.pi*AR))*np.sin(
            theta_n[i])*(np.sin(theta_n[i])+k[i]) for i in range(N)]
        RHS =[[np.sin((j+1)*theta_n[i])*(np.sin(theta_n[i])+(j+1)*k[i]) for j in range(1,N)]+[-k[i]*np.sin(theta_n[i])] for i in range(N)]
        # solving equation
        RHS = np.array(RHS)
        LHS = np.array(LHS)
        A = np.linalg.solve(RHS, LHS)
        coefeq28 = [sum([4*A[j]*np.sin((j+2)*theta_n[i]) for j in range(N-1)])+4*A1*np.sin(theta_n[i]) for i in range(N)]
        calculated_cl = [span*coefeq28[i]/cordes[i] for i in range(N)] #found cl
        final_cl = calculated_cl
        # new lcslp list and new zlaof list
        cs_cl.extrapolate = False #see line 78
        c_aoa = np.array([cs_cl.solve(calculated_cl[i]) for i in range(N)]) #angles of attack corresponding to these calculated cl
        for i in range(N):
            try:
                c_aoa[i]= float(c_aoa[i])
            except TypeError:
                if c_aoa[i].size == 0: #since cs.cl.exptrapolate = False (line42), an empty list means there is a stall
                    print("warning, stall at ",etha_n[i]*100, "semi_span (rang ", i, ")")
                    c_aoa[i] = np.nan
                    os.system("pause")
                else: exit()
        n_lcslp = np.array([float(cs_cl(c_aoa[i], 1)) for i in range(N)]) #new lift curve slope list
        n_zlaoa = np.array([float(c_aoa[i]-calculated_cl[i]/n_lcslp[i]) for i in range(N)]) #new zero lift angle of attack lift
        if(max(abs(zlaoa-n_zlaoa)) < 0.00001 and max(abs(lcslp-n_lcslp)) < 0.00001):#convergence criteria
            break
        zlaoa = n_zlaoa
        lcslp = n_lcslp
        aoa = A[-1]
    final_cl = np.array([round(final_cl[i], 3) for i in range(N)], dtype =float)
    #sectional moment coefficient
    final_cm = np.array([cs_cm(c_aoa[i]) for i in range(N)])
    #sectional zero lift drag coefficient
    final_cd = np.array([cs_cd(c_aoa[i]) for i in range(N)])
    #induiced angle of attack (rad)
    alfa_i = np.array([round(sum([(j+1)*A[j]*np.sin((j+1)*theta_n[i])/np.sin(theta_n[i]) for j in range(N)])+A1,2) for i in range(N)],dtype = float)
    """print("Induced drag (in degree)")
    print(alfa_i*180/np.pi)"""
    # sectional vortex (induced) drag coefficient
    cdv = np.array([round(final_cl[i]*alfa_i[i], 4) for i in range(N)])
    #total vortex (induced) drag coefficient
    CDV = sum([cdv[i]*AR*etha_m[i] for i in range(N)])
    #total zero lift drag coefficient
    CDo = sum([final_cd[i]*etha_m[i] for i in range(N)])
    #total moment coefficient
    CM = sum([final_cm[i]*etha_m[i] for i in range(N)])
    print("total wing vortex drag coeff")
    print(CDV)
    print("total wing zero lift drag coeff")
    print(CDo)
    print("Aircraft moment coefficient")
    print(CM)
    print("Cl for aoa = ", aoa)
    Cl = A1*np.pi*AR
    print(Cl)
    k = CDV/(Cl**2) #CDV = k*Cl^2
    print("k obtained: ")
    print(k)
    print("e obtained")
    print(Cl**2/(np.pi*CDV*AR))
    return float(Cl),float(k),float(CDo),float(CM)