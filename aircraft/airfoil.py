from pathlib import Path
import numpy as np


class Airfoil:
    def __init__(self,name):
        self.name = name
        self.load_coordinates()
        self.set_characteristics()
        
    def load_coordinates(self):
        project_root = Path(__file__).resolve().parents[1]
        path = project_root / "data" / f"{self.name}.txt"

        if not path.exists():
            raise FileNotFoundError(f"Airfoil coordinate file not found: {path}")
        x = []
        y = []

        with open(path, "r", encoding = "utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                values = line.split()

                try:
                    x_value = float(values[0])
                    y_value = float(values[1])
                except (ValueError, IndexError):
                    continue
                x.append(x_value)
                y.append(y_value)
        self.coordinates = np.array(x), np.array(y)

    def set_characteristics(self):
        if self.name =="ishii":
            self.la_unit = 0.0509 #m^2
            self.cla_unit = 0.4148 #m
            self.cl_max = 1.1244 #defautl

        elif self.name == "naca0007":
            self.la_unit = 0.064 #m^2
            self.cla_unit = 0.471 #m
            self.cl_max = 1.0 #default
        else:
            raise ValueError(f"Unknown airfoil: {self.name}")
        
    def update_cl_max_from_xfoil(self, reynolds, mach=0.0):
        computed_cl_max = ...
        self.cl_max = computed_cl_max