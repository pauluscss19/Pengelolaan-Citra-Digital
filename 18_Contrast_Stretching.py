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
    print_rgb_before_after,
    draw_histogram_manual,
    save_matrix_as_image
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
P4 NOMOR 4 - CONTRAST STRETCHING

s = ((r-rmin)/(rmax-rmin))*255

BEFORE = grayscale
AFTER  = grayscale setelah stretching.
"""


def find_minmax(gray):
    rmin = 255
    rmax = 0

    for row in gray:
        for value in row:
            if value < rmin:
                rmin = value
            if value > rmax:
                rmax = value

    return rmin, rmax

def clamp(val):
    if val < 0:
        return 0
    elif val > 255:
        return 255
    return int(round(val))


def stretch(gray, rmin, rmax):
    result = []

    for row in gray:
        out = []

        for r in row:
            if rmax == rmin:
                s = r
            else:
                s = ((r-rmin)/(rmax-rmin))*255

            out.append(clamp(s))

        result.append(out)

    return result


def main():
    print("\nP4 NOMOR 4 - CONTRAST STRETCHING")

    _, gray = load_gray(IMAGE_1)

    rmin, rmax = find_minmax(gray)
    result = stretch(gray, rmin, rmax)

    new_min, new_max = find_minmax(result)

    print("rmin sebelum =", rmin)
    print("rmax sebelum =", rmax)
    print("rmin sesudah =", new_min)
    print("rmax sesudah =", new_max)

    print_grayscale_before_after(
        gray,
        result,
        "BEFORE - ORIGINAL",
        "AFTER - STRETCHING"
    )

    def get_hist(matrix):
        h = [0 for _ in range(256)]
        for row in matrix:
            for v in row: h[v] += 1
        return h

    # Simpan juga grafiknya sebagai file terpisah
    save_matrix_as_image(draw_histogram_manual(get_hist(gray)), "GRAFIK_SEBELUM_STRETCHING", is_rgb=False)
    save_matrix_as_image(draw_histogram_manual(get_hist(result)), "GRAFIK_SESUDAH_STRETCHING", is_rgb=False)


if __name__ == "__main__":
    main()
