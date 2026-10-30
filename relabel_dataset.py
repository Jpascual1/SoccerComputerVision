import shutil
import sys
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / "football-players-detection"
OUTPUT = BASE_DIR / "football-players-detection-relabeled"

# Old class id -> new class id (ball, goalkeeper, player, referee -> Ball, Player, Referee)
CLASS_MAP = {0: 0, 1: 1, 2: 1, 3: 2}
NEW_NAMES = ["Ball", "Player", "Referee"]
SPLITS = ["train", "valid", "test"]


def count_classes(dataset: Path) -> Counter:
    counts = Counter()
    for label_file in dataset.glob("*/labels/*.txt"):
        for line in label_file.read_text().splitlines():
            if line.strip():
                counts[int(line.split()[0])] += 1
    return counts


def remap_label_file(src: Path, dst: Path) -> None:
    new_lines = []
    for line_number, line in enumerate(src.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        class_id, rest = line.split(maxsplit=1)
        if int(class_id) not in CLASS_MAP:
            sys.exit(f"Unknown class {class_id} in {src} line {line_number}")
        new_lines.append(f"{CLASS_MAP[int(class_id)]} {rest}")
    dst.write_text("\n".join(new_lines) + ("\n" if new_lines else ""))


def write_data_yaml(src: Path, dst: Path) -> None:
    lines = []
    for line in src.read_text().splitlines():
        if line.startswith("nc:"):
            line = f"nc: {len(NEW_NAMES)}"
        elif line.startswith("names:"):
            line = f"names: {NEW_NAMES}"
        lines.append(line)
    dst.write_text("\n".join(lines) + "\n")


if OUTPUT.exists():
    sys.exit(f"{OUTPUT} already exists. Delete it to rebuild the relabeled dataset.")

print("Before:", dict(sorted(count_classes(SOURCE).items())))

for split in SPLITS:
    split_dir = SOURCE / split
    if not split_dir.is_dir():
        continue
    shutil.copytree(split_dir / "images", OUTPUT / split / "images")
    (OUTPUT / split / "labels").mkdir(parents=True)
    for label_file in sorted((split_dir / "labels").glob("*.txt")):
        remap_label_file(label_file, OUTPUT / split / "labels" / label_file.name)

write_data_yaml(SOURCE / "data.yaml", OUTPUT / "data.yaml")
for readme in SOURCE.glob("README*.txt"):
    shutil.copy2(readme, OUTPUT / readme.name)

after = count_classes(OUTPUT)
print("After: ", {NEW_NAMES[class_id]: count for class_id, count in sorted(after.items())})
print(f"Relabeled dataset written to {OUTPUT}")
