from pathlib import Path

project_root = Path(__file__).resolve().parents[1]

input_file = project_root / "data" / "ishii.txt"
output_file = project_root / "data" / "ishii_xfoil.dat"

points = []

with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        if not line:
            continue

        parts = line.replace(",", ".").split()

        if len(parts) < 2:
            continue

        x = float(parts[0])
        y = float(parts[1])

        point = (x, y)

        # remove consecutive duplicate points
        if not points or point != points[-1]:
            points.append(point)

# remove duplicate leading/trailing issue if first and last are identical
if len(points) > 1 and points[0] == points[-1]:
    points.pop()

with open(output_file, "w", encoding="utf-8") as file:
    file.write("Ishii\n")
    for x, y in points:
        file.write(f"{x:.7f} {y:.7f}\n")

print(f"Created: {output_file}")
print(f"Number of points: {len(points)}")
print("First 5 points:")
for point in points[:5]:
    print(point)
print("Last 5 points:")
for point in points[-5:]:
    print(point)