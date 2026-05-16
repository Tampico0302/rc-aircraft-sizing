class Air:
    def __init__(self,rho,vc,vs,mu):
        self.rho = rho
        self.vc = vc #cruise speed m/s
        self.vs = vs #stall speed m/s
        self.mu = mu   #dynamic viscosity Pa.s