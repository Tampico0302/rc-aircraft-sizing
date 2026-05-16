from pathlib import Path
import shutil
import subprocess


project_root = Path(__file__).resolve().parents[1]

xfoil_exe = Path(r"C:\Xfoil\xfoil.exe")
workdir = project_root / "xfoil_work"
workdir.mkdir(exist_ok=True)

source_airfoil = project_root / "data" / "ishii_xfoil.dat"
local_airfoil = workdir / "ishii_xfoil.dat"

shutil.copy(source_airfoil, local_airfoil)

polar_file = workdir / "ishii_polar.txt"

if polar_file.exists():
    polar_file.unlink()

commands = "\n".join([
    "LOAD ishii_xfoil.dat",
    "PANE",
    "OPER",
    "VISC 100000",
    "MACH 0.0",
    "ITER 100",
    "PACC",
    "ishii_polar.txt",
    "",
    "ASEQ -2 15 1",
    "PACC",
    "",
    "QUIT",
    "",
])

result = subprocess.run(
    [str(xfoil_exe)],
    input=commands,
    text=True,
    capture_output=True,
    cwd=workdir,
)

print(result.stdout)

if result.stderr:
    print("STDERR:")
    print(result.stderr)

if polar_file.exists():
    print("\nXFOIL check successful.")
    print(f"Polar file created: {polar_file}")

    print("\nPolar file preview:")
    print(polar_file.read_text(errors="ignore")[:2000])
else:
    print("\nXFOIL check failed: polar file was not created.")