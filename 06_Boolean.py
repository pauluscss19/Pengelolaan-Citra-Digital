"""
PRAKTIKUM PENGOLAHAN CITRA - MULBERRY
Versi visual terminal: BEFORE vs AFTER.

Pillow hanya untuk membaca JPG/PNG.
Perhitungan citra dibuat manual.
"""

from pathlib import Path
from PIL import Image

from terminal_image import (
    print_grayscale_before_after,
    print_rgb_before_after
)

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "Mulberry"

if not DATASET_DIR.exists():
    DATASET_DIR = BASE_DIR.parent / "Mulberry"

if not DATASET_DIR.exists():
    raise FileNotFoundError(
        "Folder Mulberry tidak ditemukan. "
        "Letakkan folder Mulberry satu folder dengan script "
        "atau satu level di atas folder script."
    )

IMAGE_1 = DATASET_DIR / "Healthy" / "healthy01.jpg"
IMAGE_2 = DATASET_DIR / "Leaf_Rust" / "rust01.jpg"

SAMPLE_STEP = 4


def load_rgb(path):
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    image = Image.open(path).convert("RGB")
    width, height = image.size
    px = image.load()

    rgb = []

    for y in range(height):
        row = []
        for x in range(width):
            row.append(px[x, y])
        rgb.append(row)

    return rgb


def sample_rgb(rgb, step):
    result = []

    i = 0
    while i < len(rgb):
        row = []

        j = 0
        while j < len(rgb[0]):
            row.append(rgb[i][j])
            j += step

        result.append(row)
        i += step

    return result


def rgb_to_gray_manual(rgb):
    result = []

    for row in rgb:
        out = []

        for r, g, b in row:
            y = 0.299*r + 0.587*g + 0.144*b

            if y < 0:
                y = 0
            elif y > 255:
                y = 255

            out.append(int(round(y)))

        result.append(out)

    return result


def threshold_manual(gray, threshold):
    result = []

    for row in gray:
        out = []

        for value in row:
            if value < threshold:
                out.append(0)
            else:
                out.append(1)

        result.append(out)

    return result


def binary_to_rgb(binary):
    result = []

    for row in binary:
        out = []

        for value in row:
            if value == 1:
                out.append((255, 255, 255))
            else:
                out.append((0, 0, 0))

        result.append(out)

    return result


def load_gray(path):
    raw = load_rgb(path)
    rgb = sample_rgb(raw, SAMPLE_STEP)
    gray = rgb_to_gray_manual(rgb)
    return rgb, gray


def same_size(a, b):
    return len(a) == len(b) and len(a[0]) == len(b[0])


def matrix_minmax(a):
    mn = 255
    mx = 0

    for row in a:
        for value in row:
            if value < mn:
                mn = value
            if value > mx:
                mx = value

    return mn, mx


def print_info(gray):
    h = len(gray)
    w = len(gray[0])
    mn, mx = matrix_minmax(gray)
    print(f"Ukuran kerja : {w} x {h}")
    print(f"Min intensitas: {mn}")
    print(f"Max intensitas: {mx}")


"""
P3 NOMOR 6 - BOOLEAN

Operasi:
AND, OR, NOT, XOR

Input adalah hasil thresholding.
"""
T = 128


def boolean_manual(a, b):
    and_img = []
    or_img = []
    not_img = []
    xor_img = []

    for i in range(len(a)):
        row_and = []
        row_or = []
        row_not = []
        row_xor = []

        for j in range(len(a[0])):
            av = a[i][j]
            bv = b[i][j]

            row_and.append(1 if av == 1 and bv == 1 else 0)
            row_or.append(1 if av == 1 or bv == 1 else 0)
            row_not.append(1 if av == 0 else 0)
            row_xor.append(1 if av != bv else 0)

        and_img.append(row_and)
        or_img.append(row_or)
        not_img.append(row_not)
        xor_img.append(row_xor)

    return and_img, or_img, not_img, xor_img


def binary_to_gray(binary):
    return [
        [255 if value == 1 else 0 for value in row]
        for row in binary
    ]


def main():
    print("\nP3 NOMOR 6 - BOOLEAN")

    _, a_gray = load_gray(IMAGE_1)
    _, b_gray = load_gray(IMAGE_2)

    a = threshold_manual(a_gray, T)
    b = threshold_manual(b_gray, T)

    if not same_size(a, b):
        raise ValueError("Ukuran kedua citra harus sama.")

    and_img, or_img, not_img, xor_img = boolean_manual(a, b)

    print_grayscale_before_after(
        binary_to_gray(a),
        binary_to_gray(and_img),
        "BEFORE - A",
        "AFTER - AND"
    )

    print_grayscale_before_after(
        binary_to_gray(a),
        binary_to_gray(or_img),
        "BEFORE - A",
        "AFTER - OR"
    )

    print_grayscale_before_after(
        binary_to_gray(a),
        binary_to_gray(not_img),
        "BEFORE - A",
        "AFTER - NOT"
    )

    print_grayscale_before_after(
        binary_to_gray(a),
        binary_to_gray(xor_img),
        "BEFORE - A",
        "AFTER - XOR"
    )


if __name__ == "__main__":
    main()
