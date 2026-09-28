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
P4 NOMOR 5 - HISTOGRAM EQUALIZATION

Tahap:
1. Histogram
2. CDF
3. Mapping
4. Terapkan mapping

Ko = round(Ci*255/(w*h))
"""


def histogram_manual(gray):
    hist = [0 for _ in range(256)]

    for row in gray:
        for value in row:
            hist[value] += 1

    return hist


def cdf_manual(hist):
    cdf = [0 for _ in range(256)]

    cdf[0] = hist[0]

    for i in range(1, 256):
        cdf[i] = cdf[i-1] + hist[i]

    return cdf

def clamp(val):
    if val < 0:
        return 0
    elif val > 255:
        return 255
    return int(round(val))


def mapping_manual(cdf, total):
    mapping = [0 for _ in range(256)]

    for i in range(256):
        mapping[i] = clamp(
            round(cdf[i]*255/total)
        )

    return mapping


def apply_mapping(gray, mapping):
    result = []

    for row in gray:
        out = []

        for value in row:
            out.append(mapping[value])

        result.append(out)

    return result


def main():
    print("\nP4 NOMOR 5 - HISTOGRAM EQUALIZATION")

    _, gray = load_gray(IMAGE_1)

    hist = histogram_manual(gray)
    total = len(gray)*len(gray[0])

    cdf = cdf_manual(hist)
    mapping = mapping_manual(cdf, total)

    equalized = apply_mapping(gray, mapping)

    print_grayscale_before_after(
        gray,
        equalized,
        "BEFORE - ORIGINAL",
        "AFTER - EQUALIZATION"
    )

    def get_hist(matrix):
        h = [0 for _ in range(256)]
        for row in matrix:
            for v in row: h[v] += 1
        return h

    # Simpan juga grafiknya sebagai file terpisah
    save_matrix_as_image(draw_histogram_manual(get_hist(gray)), "GRAFIK_SEBELUM_EQUALIZATION", is_rgb=False)
    save_matrix_as_image(draw_histogram_manual(get_hist(equalized)), "GRAFIK_SESUDAH_EQUALIZATION", is_rgb=False)

    print("\nINTENSITAS | HIST | CDF | MAPPING")

    shown = 0

    for i in range(256):
        if hist[i] > 0:
            print(
                f"{i:>10} | "
                f"{hist[i]:>5} | "
                f"{cdf[i]:>7} | "
                f"{mapping[i]:>7}"
            )

            shown += 1

            if shown >= 30:
                print("... ditampilkan 30 intensitas pertama ...")
                break


if __name__ == "__main__":
    main()
