from pathlib import Path
import argparse


def prepare_airfoil_for_xfoil(airfoil_name):
    project_root = Path(__file__).resolve().parents[1]

    input_file = project_root / "data" / f"{airfoil_name}.txt"
    output_file = project_root / "data" / f"{airfoil_name}_xfoil.dat"

    if not input_file.exists():
        raise FileNotFoundError(f"Input airfoil file not found: {input_file}")

    points = []

    with open(input_file, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            parts = line.replace(",", ".").split()

            if len(parts) < 2:
                continue

            try:
                x = float(parts[0])
                y = float(parts[1])
            except ValueError:
                continue

            point = (x, y)

            # Remove consecutive duplicate points
            if not points or point != points[-1]:
                points.append(point)

    # Remove duplicate first/last point if present
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()

    if len(points) < 3:
        raise ValueError("Not enough valid coordinate points were found.")

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"{airfoil_name}\n")

        for x, y in points:
            file.write(f"{x:.7f} {y:.7f}\n")

    print(f"Created: {output_file}")
    print(f"Number of points: {len(points)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepare an airfoil coordinate file for XFOIL."
    )

    parser.add_argument(
        "airfoil_name",
        help="Airfoil name without extension. Example: ishii for data/ishii.txt",
    )

    args = parser.parse_args()

    prepare_airfoil_for_xfoil(args.airfoil_name)