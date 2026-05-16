from pathlib import Path
import subprocess


def write_airfoil_dat(coordinates, output_file, airfoil_name="Current airfoil"):
    x, y = coordinates

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"{airfoil_name}\n")

        for xi, yi in zip(x, y):
            file.write(f"{float(xi):.7f} {float(yi):.7f}\n")


def run_xfoil(
    coordinates,
    reynolds,
    mach=0.0,
    alpha_start=-3.0,
    alpha_end=15.0,
    alpha_step=0.25,
    xfoil_exe_path=r"C:\Xfoil\xfoil.exe",
):
    project_root = Path(__file__).resolve().parents[1]

    workdir = project_root / "xfoil_work"
    workdir.mkdir(exist_ok=True)

    xfoil_exe = Path(xfoil_exe_path)

    if not xfoil_exe.exists():
        raise FileNotFoundError(f"XFOIL executable not found: {xfoil_exe}")

    airfoil_file = workdir / "current_airfoil.dat"
    polar_file = workdir / "current_airfoil_polar.txt"

    if polar_file.exists():
        polar_file.unlink()

    write_airfoil_dat(
        coordinates=coordinates,
        output_file=airfoil_file,
        airfoil_name="Current airfoil",
    )

    commands = "\n".join([
        f"LOAD {airfoil_file.name}",
        "PANE",
        "OPER",
        f"VISC {reynolds}",
        f"MACH {mach}",
        "ITER 100",
        "PACC",
        polar_file.name,
        "",
        f"ASEQ {alpha_start} {alpha_end} {alpha_step}",
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

    if not polar_file.exists():
        raise RuntimeError(
            "XFOIL did not create the polar file.\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    return polar_file