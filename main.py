"""
P3 + P4 - PENGOLAHAN CITRA MANUAL
Dataset: Mulberry Leaf Dataset
Struktur folder:

Mulberry/
├── Healthy/
│   ├── healthy01.jpg
│   └── healthy02.jpg
├── Leaf_Rust/
│   ├── rust01.jpg
│   └── rust02.jpg
└── Leaf_Spot/
    ├── spot01.jpg
    └── spot02.jpg

ATURAN IMPLEMENTASI:
- Pillow (PIL) hanya dipakai untuk BACA/SIMPAN gambar.
- Tidak memakai OpenCV, NumPy, SciPy, scikit-image, dll.
- Tidak memakai fungsi siap jadi seperti grayscale/threshold/resize/
  rotate/flip/histogram/equalization.
- Operasi citra dibuat manual dengan list, loop, if, dan rumus.
"""

from pathlib import Path
from PIL import Image, ImageDraw

# ============================================================
# 0. PENGATURAN
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "Mulberry"
OUTPUT_DIR = BASE_DIR / "Hasil"

# Gunakan 1 untuk ukuran asli. Karena Mulberry sangat besar,
# 4 lebih aman untuk praktik lokal. Data mentah tidak diubah.
SAMPLE_STEP = 4

THRESHOLD = 128
BRIGHTNESS_VALUE = 50
SHIFT_X = 50
SHIFT_Y = 30
ZOOM_FACTOR = 2

IMAGE_1 = DATASET_DIR / "Healthy" / "healthy01.jpg"
IMAGE_2 = DATASET_DIR / "Leaf_Rust" / "rust01.jpg"

MAX_HIST_HEIGHT = 400
HIST_WIDTH = 768
HIST_HEIGHT = 480


# ============================================================
# UTILITAS DASAR
# ============================================================

def ensure_dirs():
    (OUTPUT_DIR / "P3").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "P4").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "Data_Proses").mkdir(parents=True, exist_ok=True)


def load_rgb(path):
    if not path.exists():
        raise FileNotFoundError(f"File tidak ditemukan: {path}")

    img = Image.open(path).convert("RGB")
    width, height = img.size

    pixels = list(img.getdata())

    rgb = []
    idx = 0
    for _y in range(height):
        row = []
        for _x in range(width):
            row.append(pixels[idx])
            idx += 1
        rgb.append(row)

    return rgb, width, height


def save_rgb(path, rgb):
    height = len(rgb)
    width = len(rgb[0]) if height > 0 else 0

    flat = []
    for i in range(height):
        for j in range(width):
            r, g, b = rgb[i][j]
            flat.append((
                clamp_int(r, 0, 255),
                clamp_int(g, 0, 255),
                clamp_int(b, 0, 255)
            ))

    img = Image.new("RGB", (width, height))
    img.putdata(flat)
    img.save(path)


def save_gray(path, gray):
    height = len(gray)
    width = len(gray[0]) if height > 0 else 0

    flat = []
    for i in range(height):
        for j in range(width):
            value = clamp_int(gray[i][j], 0, 255)
            flat.append((value, value, value))

    img = Image.new("RGB", (width, height))
    img.putdata(flat)
    img.save(path)


def clamp_int(value, low, high):
    if value < low:
        return low
    if value > high:
        return high
    return int(round(value))


# ============================================================
# MANUAL DOWNSAMPLING UNTUK WORKING COPY
# ============================================================

def downsample_pick_rgb(rgb, step):
    if step < 1:
        raise ValueError("SAMPLE_STEP harus >= 1.")

    height = len(rgb)
    width = len(rgb[0])

    result = []

    i = 0
    while i < height:
        row = []
        j = 0
        while j < width:
            row.append(rgb[i][j])
            j += step
        result.append(row)
        i += step

    return result


# ============================================================
# P3.1 RGB -> GRAYSCALE
# Mengikuti rumus pada materi:
# Y = 0.299R + 0.587G + 0.144B
# ============================================================

def rgb_to_gray_manual(rgb):
    height = len(rgb)
    width = len(rgb[0])

    gray = []

    for i in range(height):
        row = []
        for j in range(width):
            r, g, b = rgb[i][j]

            value = (
                0.299 * r +
                0.587 * g +
                0.144 * b
            )

            row.append(clamp_int(value, 0, 255))
        gray.append(row)

    return gray


# ============================================================
# P3.2 THRESHOLDING
# f(x,y) < T -> 0
# f(x,y) >= T -> 1
# ============================================================

def threshold_manual(gray, threshold):
    height = len(gray)
    width = len(gray[0])

    binary = []

    for i in range(height):
        row = []
        for j in range(width):
            if gray[i][j] < threshold:
                row.append(0)
            else:
                row.append(1)
        binary.append(row)

    return binary


def save_binary(path, binary):
    height = len(binary)
    width = len(binary[0])

    flat = []

    for i in range(height):
        for j in range(width):
            value = 255 if binary[i][j] == 1 else 0
            flat.append((value, value, value))

    img = Image.new("RGB", (width, height))
    img.putdata(flat)
    img.save(path)


# ============================================================
# P3.3 NEGATIVE
# f' = 255 - f
# ============================================================

def negative_manual(gray):
    height = len(gray)
    width = len(gray[0])

    result = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append(255 - gray[i][j])
        result.append(row)

    return result


# ============================================================
# P3.4 BRIGHTENING
# f' = f + b, dengan clipping
# ============================================================

def brightening_manual(gray, b):
    height = len(gray)
    width = len(gray[0])

    result = []

    for i in range(height):
        row = []
        for j in range(width):
            value = gray[i][j] + b
            row.append(clamp_int(value, 0, 255))
        result.append(row)

    return result


# ============================================================
# P3.5 ARITMETIKA DUA CITRA
# ============================================================

def check_same_size(a, b):
    if len(a) != len(b):
        raise ValueError("Tinggi kedua citra berbeda.")

    if len(a[0]) != len(b[0]):
        raise ValueError("Lebar kedua citra berbeda.")


def addition_manual(a, b):
    check_same_size(a, b)

    height = len(a)
    width = len(a[0])
    result = []

    for i in range(height):
        row = []
        for j in range(width):
            value = a[i][j] + b[i][j]
            row.append(clamp_int(value, 0, 255))
        result.append(row)

    return result


def subtraction_binary_manual(a, b):
    check_same_size(a, b)

    height = len(a)
    width = len(a[0])
    result = []

    for i in range(height):
        row = []
        for j in range(width):
            value = a[i][j] - b[i][j]

            if value != 0:
                row.append(255)
            else:
                row.append(0)

        result.append(row)

    return result


def multiplication_manual(a, b):
    check_same_size(a, b)

    height = len(a)
    width = len(a[0])
    result = []

    for i in range(height):
        row = []
        for j in range(width):
            value = a[i][j] * b[i][j]
            row.append(clamp_int(value, 0, 255))
        result.append(row)

    return result


def scalar_multiply_manual(gray, c):
    height = len(gray)
    width = len(gray[0])
    result = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append(clamp_int(gray[i][j] * c, 0, 255))
        result.append(row)

    return result


def scalar_divide_manual(gray, c):
    if c == 0:
        raise ValueError("Tidak boleh membagi dengan nol.")

    height = len(gray)
    width = len(gray[0])
    result = []

    for i in range(height):
        row = []
        for j in range(width):
            row.append(clamp_int(gray[i][j] / c, 0, 255))
        result.append(row)

    return result


# ============================================================
# P3.6 BOOLEAN
# ============================================================

def boolean_manual(a, b):
    check_same_size(a, b)

    height = len(a)
    width = len(a[0])

    and_img = []
    or_img = []
    not_img = []
    xor_img = []

    for i in range(height):
        row_and = []
        row_or = []
        row_not = []
        row_xor = []

        for j in range(width):
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


# ============================================================
# P3.7 OPERASI LOKAL
# Konvolusi 3x3 manual
# ============================================================

def convolution_manual(gray, kernel):
    height = len(gray)
    width = len(gray[0])

    result = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(1, height - 1):
        for j in range(1, width - 1):

            total = 0.0

            for ki in range(3):
                for kj in range(3):
                    pixel = gray[i + ki - 1][j + kj - 1]
                    total += pixel * kernel[ki][kj]

            result[i][j] = total

    return result


# ============================================================
# P3.8 TRANSLASI
# ============================================================

def translation_manual(gray, dx, dy):
    height = len(gray)
    width = len(gray[0])

    result = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):

            new_i = i + dy
            new_j = j + dx

            if (
                0 <= new_i < height and
                0 <= new_j < width
            ):
                result[new_i][new_j] = gray[i][j]

    return result


# ============================================================
# P3.9 ROTASI 90 CW DAN CCW
# ============================================================

def rotate90_cw_manual(gray):
    height = len(gray)
    width = len(gray[0])

    result = [[0 for _ in range(height)] for _ in range(width)]

    for i in range(height):
        for j in range(width):
            result[j][height - i - 1] = gray[i][j]

    return result


def rotate90_ccw_manual(gray):
    height = len(gray)
    width = len(gray[0])

    result = [[0 for _ in range(height)] for _ in range(width)]

    for i in range(height):
        for j in range(width):
            result[width - j - 1][i] = gray[i][j]

    return result


# ============================================================
# P3.10 FLIPPING
# ============================================================

def flip_horizontal_manual(gray):
    height = len(gray)
    width = len(gray[0])

    result = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            result[i][width - j - 1] = gray[i][j]

    return result


def flip_vertical_manual(gray):
    height = len(gray)
    width = len(gray[0])

    result = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            result[height - i - 1][j] = gray[i][j]

    return result


# ============================================================
# P3.11 ZOOMING - NEAREST NEIGHBOR
# ============================================================

def zoom_nearest_manual(gray, factor):
    height = len(gray)
    width = len(gray[0])

    new_height = height * factor
    new_width = width * factor

    result = [[0 for _ in range(new_width)] for _ in range(new_height)]

    for i in range(height):
        for j in range(width):

            for di in range(factor):
                for dj in range(factor):

                    result[
                        i * factor + di
                    ][
                        j * factor + dj
                    ] = gray[i][j]

    return result


# ============================================================
# P3.12 DOWNSAMPLING 1/2 DENGAN RATA-RATA 4 PIXEL
# ============================================================

def downsample_average2_manual(gray):
    height = len(gray)
    width = len(gray[0])

    new_height = height // 2
    new_width = width // 2

    result = [[0 for _ in range(new_width)] for _ in range(new_height)]

    for i in range(new_height):
        for j in range(new_width):

            p1 = gray[2 * i][2 * j]
            p2 = gray[2 * i][2 * j + 1]
            p3 = gray[2 * i + 1][2 * j]
            p4 = gray[2 * i + 1][2 * j + 1]

            average = (p1 + p2 + p3 + p4) / 4

            result[i][j] = clamp_int(average, 0, 255)

    return result


# ============================================================
# P3.13 BILINEAR INTERPOLATION 2x
# ============================================================

def bilinear_resize_manual(gray, factor):
    height = len(gray)
    width = len(gray[0])

    new_height = height * factor
    new_width = width * factor

    result = [[0 for _ in range(new_width)] for _ in range(new_height)]

    for y_new in range(new_height):
        for x_new in range(new_width):

            x = x_new / factor
            y = y_new / factor

            x1 = int(x)
            y1 = int(y)

            x2 = x1 + 1
            y2 = y1 + 1

            if x2 >= width:
                x2 = width - 1

            if y2 >= height:
                y2 = height - 1

            dx = x - x1
            dy = y - y1

            q11 = gray[y1][x1]
            q21 = gray[y1][x2]
            q12 = gray[y2][x1]
            q22 = gray[y2][x2]

            r1 = (1 - dx) * q11 + dx * q21
            r2 = (1 - dx) * q12 + dx * q22

            value = (1 - dy) * r1 + dy * r2

            result[y_new][x_new] = clamp_int(value, 0, 255)

    return result


# ============================================================
# P4.1 HISTOGRAM GRAYSCALE MANUAL
# indeks 0..255
# ============================================================

def histogram_gray_manual(gray):
    histogram = [0 for _ in range(256)]

    height = len(gray)
    width = len(gray[0])

    for i in range(height):
        for j in range(width):
            value = clamp_int(gray[i][j], 0, 255)
            histogram[value] += 1

    return histogram


# ============================================================
# P4.2 HISTOGRAM RGB MANUAL
# ============================================================

def histogram_rgb_manual(rgb):
    hist_r = [0 for _ in range(256)]
    hist_g = [0 for _ in range(256)]
    hist_b = [0 for _ in range(256)]

    height = len(rgb)
    width = len(rgb[0])

    for i in range(height):
        for j in range(width):

            r, g, b = rgb[i][j]

            hist_r[r] += 1
            hist_g[g] += 1
            hist_b[b] += 1

    return hist_r, hist_g, hist_b


# ============================================================
# P4.3 NORMALISASI HISTOGRAM
# h_i = n_i / n
# ============================================================

def normalize_histogram_manual(histogram, total_pixels):
    return [value / total_pixels for value in histogram]


# ============================================================
# P4.4 CONTRAST STRETCHING
# s = ((r-rmin)/(rmax-rmin))*255
# ============================================================

def find_minmax_manual(gray):
    rmin = 255
    rmax = 0

    height = len(gray)
    width = len(gray[0])

    for i in range(height):
        for j in range(width):

            value = gray[i][j]

            if value < rmin:
                rmin = value

            if value > rmax:
                rmax = value

    return rmin, rmax


def contrast_stretch_manual(gray, rmin, rmax):
    height = len(gray)
    width = len(gray[0])

    result = []

    for i in range(height):
        row = []

        for j in range(width):

            r = gray[i][j]

            if rmax == rmin:
                s = r
            else:
                s = ((r - rmin) / (rmax - rmin)) * 255

            row.append(clamp_int(s, 0, 255))

        result.append(row)

    return result


# ============================================================
# P4.5 HISTOGRAM EQUALIZATION
#
# CDF = cumulative histogram
# Ko = round(Ci * 255 / (w*h))
# Mengikuti bentuk perhitungan pada materi.
# ============================================================

def histogram_equalization_manual(gray):
    histogram = histogram_gray_manual(gray)

    height = len(gray)
    width = len(gray[0])
    total_pixels = height * width

    cdf = [0 for _ in range(256)]

    cdf[0] = histogram[0]

    for k in range(1, 256):
        cdf[k] = cdf[k - 1] + histogram[k]

    mapping = [0 for _ in range(256)]

    for k in range(256):
        ko = round((cdf[k] * 255) / total_pixels)
        mapping[k] = clamp_int(ko, 0, 255)

    result = []

    for i in range(height):
        row = []

        for j in range(width):
            original_value = gray[i][j]
            row.append(mapping[original_value])

        result.append(row)

    return result, cdf, mapping


# ============================================================
# OUTPUT HISTOGRAM DENGAN PILLOW
# Hanya visualisasi. Perhitungan histogram tetap manual.
# ============================================================

def save_histogram_png(path, histogram, title, normalized=False):
    canvas = Image.new(
        "RGB",
        (HIST_WIDTH, HIST_HEIGHT),
        (255, 255, 255)
    )

    draw = ImageDraw.Draw(canvas)

    left = 60
    right = 20
    top = 50
    bottom = 60

    plot_w = HIST_WIDTH - left - right
    plot_h = HIST_HEIGHT - top - bottom

    max_value = max(histogram) if histogram else 1

    if max_value == 0:
        max_value = 1

    draw.text((left, 15), title, fill=(0, 0, 0))

    # Sumbu
    draw.line(
        (left, top + plot_h, left + plot_w, top + plot_h),
        fill=(0, 0, 0),
        width=1
    )
    draw.line(
        (left, top, left, top + plot_h),
        fill=(0, 0, 0),
        width=1
    )

    bar_width = max(1, plot_w // 256)

    for k in range(256):

        value = histogram[k]

        bar_h = int(
            (value / max_value) * plot_h
        )

        x1 = left + k * plot_w // 256
        x2 = left + (k + 1) * plot_w // 256

        y1 = top + plot_h - bar_h
        y2 = top + plot_h

        draw.rectangle(
            (x1, y1, max(x1, x2 - 1), y2),
            fill=(80, 80, 80)
        )

    draw.text(
        (left, HIST_HEIGHT - 40),
        "0",
        fill=(0, 0, 0)
    )
    draw.text(
        (HIST_WIDTH - right - 25, HIST_HEIGHT - 40),
        "255",
        fill=(0, 0, 0)
    )

    ylabel = "Probabilitas" if normalized else "Jumlah Piksel"

    draw.text(
        (5, top + plot_h // 2),
        ylabel,
        fill=(0, 0, 0)
    )

    canvas.save(path)


def save_histogram_csv(path, histogram):
    with path.open("w", encoding="utf-8") as f:
        f.write("intensitas,frekuensi\n")
        for i in range(256):
            f.write(f"{i},{histogram[i]}\n")


def save_normalized_histogram_csv(path, histogram_normalized):
    with path.open("w", encoding="utf-8") as f:
        f.write("intensitas,probabilitas\n")
        for i in range(256):
            f.write(f"{i},{histogram_normalized[i]:.10f}\n")


def save_mapping_csv(path, cdf, mapping):
    with path.open("w", encoding="utf-8") as f:
        f.write("intensitas,cdf,mapping_equalization\n")
        for i in range(256):
            f.write(f"{i},{cdf[i]},{mapping[i]}\n")


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    ensure_dirs()

    print("==============================================")
    print("P3 + P4 - MULBERRY LEAF - MANUAL")
    print("==============================================")
    print(f"Dataset : {DATASET_DIR}")
    print(f"Image 1 : {IMAGE_1}")
    print(f"Image 2 : {IMAGE_2}")
    print(f"Sample  : {SAMPLE_STEP}")
    print()

    # --------------------------------------------------------
    # BACA DATA MENTAH
    # --------------------------------------------------------

    rgb1_raw, raw_w1, raw_h1 = load_rgb(IMAGE_1)
    rgb2_raw, raw_w2, raw_h2 = load_rgb(IMAGE_2)

    print(f"Raw image 1 : {raw_w1} x {raw_h1}")
    print(f"Raw image 2 : {raw_w2} x {raw_h2}")

    # --------------------------------------------------------
    # WORKING COPY
    # --------------------------------------------------------

    rgb1 = downsample_pick_rgb(rgb1_raw, SAMPLE_STEP)
    rgb2 = downsample_pick_rgb(rgb2_raw, SAMPLE_STEP)

    h1 = len(rgb1)
    w1 = len(rgb1[0])

    h2 = len(rgb2)
    w2 = len(rgb2[0])

    print(f"Working 1   : {w1} x {h1}")
    print(f"Working 2   : {w2} x {h2}")

    if h1 != h2 or w1 != w2:
        raise ValueError(
            "Dua citra untuk operasi aritmetika harus berukuran sama."
        )

    # Simpan working copy
    save_rgb(
        OUTPUT_DIR / "Data_Proses" / "working_image_1.png",
        rgb1
    )
    save_rgb(
        OUTPUT_DIR / "Data_Proses" / "working_image_2.png",
        rgb2
    )

    # --------------------------------------------------------
    # P3.1 GRAYSCALE
    # --------------------------------------------------------

    print("P3.1 RGB -> Grayscale")

    gray1 = rgb_to_gray_manual(rgb1)
    gray2 = rgb_to_gray_manual(rgb2)

    save_gray(
        OUTPUT_DIR / "P3" / "01_grayscale_healthy.png",
        gray1
    )
    save_gray(
        OUTPUT_DIR / "P3" / "01_grayscale_rust.png",
        gray2
    )

    # --------------------------------------------------------
    # P3.2 THRESHOLDING
    # --------------------------------------------------------

    print("P3.2 Thresholding")

    binary1 = threshold_manual(gray1, THRESHOLD)
    binary2 = threshold_manual(gray2, THRESHOLD)

    save_binary(
        OUTPUT_DIR / "P3" / "02_threshold_healthy.png",
        binary1
    )
    save_binary(
        OUTPUT_DIR / "P3" / "02_threshold_rust.png",
        binary2
    )

    # --------------------------------------------------------
    # P3.3 NEGATIVE
    # --------------------------------------------------------

    print("P3.3 Negative")

    negative1 = negative_manual(gray1)

    save_gray(
        OUTPUT_DIR / "P3" / "03_negative.png",
        negative1
    )

    # --------------------------------------------------------
    # P3.4 BRIGHTENING
    # --------------------------------------------------------

    print("P3.4 Brightening")

    bright1 = brightening_manual(
        gray1,
        BRIGHTNESS_VALUE
    )

    save_gray(
        OUTPUT_DIR / "P3" / "04_brightening.png",
        bright1
    )

    # --------------------------------------------------------
    # P3.5 ARITMETIKA
    # --------------------------------------------------------

    print("P3.5 Arithmetic")

    add_img = addition_manual(gray1, gray2)
    sub_img = subtraction_binary_manual(gray1, gray2)
    mul_img = multiplication_manual(gray1, gray2)

    save_gray(
        OUTPUT_DIR / "P3" / "05_addition.png",
        add_img
    )

    save_gray(
        OUTPUT_DIR / "P3" / "06_subtraction.png",
        sub_img
    )

    save_gray(
        OUTPUT_DIR / "P3" / "07_multiplication.png",
        mul_img
    )

    scalar_mul = scalar_multiply_manual(gray1, 2)
    scalar_div = scalar_divide_manual(gray1, 2)

    save_gray(
        OUTPUT_DIR / "P3" / "08_scalar_multiply_2.png",
        scalar_mul
    )

    save_gray(
        OUTPUT_DIR / "P3" / "09_scalar_divide_2.png",
        scalar_div
    )

    # --------------------------------------------------------
    # P3.6 BOOLEAN
    # --------------------------------------------------------

    print("P3.6 Boolean")

    and_img, or_img, not_img, xor_img = boolean_manual(
        binary1,
        binary2
    )

    save_binary(
        OUTPUT_DIR / "P3" / "10_AND.png",
        and_img
    )

    save_binary(
        OUTPUT_DIR / "P3" / "11_OR.png",
        or_img
    )

    save_binary(
        OUTPUT_DIR / "P3" / "12_NOT.png",
        not_img
    )

    save_binary(
        OUTPUT_DIR / "P3" / "13_XOR.png",
        xor_img
    )

    # --------------------------------------------------------
    # P3.7 LOCAL OPERATION
    # --------------------------------------------------------

    print("P3.7 Local operation")

    average_kernel = [
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9]
    ]

    edge_kernel = [
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ]

    smooth = convolution_manual(
        gray1,
        average_kernel
    )

    edge = convolution_manual(
        gray1,
        edge_kernel
    )

    save_gray(
        OUTPUT_DIR / "P3" / "14_smoothing.png",
        smooth
    )

    save_gray(
        OUTPUT_DIR / "P3" / "15_edge_detection.png",
        edge
    )

    # --------------------------------------------------------
    # P3.8 TRANSLASI
    # --------------------------------------------------------

    print("P3.8 Translation")

    translated = translation_manual(
        gray1,
        SHIFT_X,
        SHIFT_Y
    )

    save_gray(
        OUTPUT_DIR / "P3" / "16_translation.png",
        translated
    )

    # --------------------------------------------------------
    # P3.9 ROTATION
    # --------------------------------------------------------

    print("P3.9 Rotation")

    rot_cw = rotate90_cw_manual(gray1)
    rot_ccw = rotate90_ccw_manual(gray1)

    save_gray(
        OUTPUT_DIR / "P3" / "17_rotation_90_CW.png",
        rot_cw
    )

    save_gray(
        OUTPUT_DIR / "P3" / "18_rotation_90_CCW.png",
        rot_ccw
    )

    # --------------------------------------------------------
    # P3.10 FLIPPING
    # --------------------------------------------------------

    print("P3.10 Flipping")

    flip_h = flip_horizontal_manual(gray1)
    flip_v = flip_vertical_manual(gray1)

    save_gray(
        OUTPUT_DIR / "P3" / "19_flip_horizontal.png",
        flip_h
    )

    save_gray(
        OUTPUT_DIR / "P3" / "20_flip_vertical.png",
        flip_v
    )

    # --------------------------------------------------------
    # P3.11 ZOOMING
    # --------------------------------------------------------

    print("P3.11 Zooming / Nearest Neighbor")

    zoom2 = zoom_nearest_manual(
        gray1,
        ZOOM_FACTOR
    )

    save_gray(
        OUTPUT_DIR / "P3" / "21_zoom_nearest_2x.png",
        zoom2
    )

    # --------------------------------------------------------
    # P3.12 DOWNSAMPLING
    # --------------------------------------------------------

    print("P3.12 Downsampling 1/2")

    small = downsample_average2_manual(gray1)

    save_gray(
        OUTPUT_DIR / "P3" / "22_downsample_average_1_2.png",
        small
    )

    # --------------------------------------------------------
    # P3.13 BILINEAR
    # --------------------------------------------------------

    print("P3.13 Bilinear 2x")

    bilinear = bilinear_resize_manual(
        gray1,
        ZOOM_FACTOR
    )

    save_gray(
        OUTPUT_DIR / "P3" / "23_bilinear_2x.png",
        bilinear
    )

    # --------------------------------------------------------
    # P4.1 GRAYSCALE HISTOGRAM
    # --------------------------------------------------------

    print("P4.1 Histogram grayscale")

    hist_gray = histogram_gray_manual(gray1)

    save_histogram_png(
        OUTPUT_DIR / "P4" / "01_histogram_grayscale.png",
        hist_gray,
        "Histogram Grayscale Manual",
        normalized=False
    )

    save_histogram_csv(
        OUTPUT_DIR / "P4" / "01_histogram_grayscale.csv",
        hist_gray
    )

    # --------------------------------------------------------
    # P4.2 RGB HISTOGRAM
    # --------------------------------------------------------

    print("P4.2 Histogram RGB")

    hist_r, hist_g, hist_b = histogram_rgb_manual(rgb1)

    save_histogram_png(
        OUTPUT_DIR / "P4" / "02_histogram_red.png",
        hist_r,
        "Histogram Red",
        normalized=False
    )

    save_histogram_png(
        OUTPUT_DIR / "P4" / "03_histogram_green.png",
        hist_g,
        "Histogram Green",
        normalized=False
    )

    save_histogram_png(
        OUTPUT_DIR / "P4" / "04_histogram_blue.png",
        hist_b,
        "Histogram Blue",
        normalized=False
    )

    save_histogram_csv(
        OUTPUT_DIR / "P4" / "02_histogram_red.csv",
        hist_r
    )

    save_histogram_csv(
        OUTPUT_DIR / "P4" / "03_histogram_green.csv",
        hist_g
    )

    save_histogram_csv(
        OUTPUT_DIR / "P4" / "04_histogram_blue.csv",
        hist_b
    )

    # --------------------------------------------------------
    # P4.3 NORMALISASI
    # --------------------------------------------------------

    print("P4.3 Histogram normalization")

    total_pixels = h1 * w1

    hist_norm = normalize_histogram_manual(
        hist_gray,
        total_pixels
    )

    save_histogram_png(
        OUTPUT_DIR / "P4" / "05_histogram_normalized.png",
        hist_norm,
        "Histogram Normalisasi",
        normalized=True
    )

    save_normalized_histogram_csv(
        OUTPUT_DIR / "P4" / "05_histogram_normalized.csv",
        hist_norm
    )

    # --------------------------------------------------------
    # P4.4 CONTRAST STRETCHING
    # --------------------------------------------------------

    print("P4.4 Contrast Stretching")

    rmin, rmax = find_minmax_manual(gray1)

    print(f"rmin = {rmin}")
    print(f"rmax = {rmax}")

    stretch = contrast_stretch_manual(
        gray1,
        rmin,
        rmax
    )

    save_gray(
        OUTPUT_DIR / "P4" / "06_contrast_stretching.png",
        stretch
    )

    hist_stretch = histogram_gray_manual(
        stretch
    )

    save_histogram_png(
        OUTPUT_DIR / "P4" / "07_histogram_after_stretching.png",
        hist_stretch,
        "Histogram Setelah Contrast Stretching",
        normalized=False
    )

    save_histogram_csv(
        OUTPUT_DIR / "P4" / "07_histogram_after_stretching.csv",
        hist_stretch
    )

    # --------------------------------------------------------
    # P4.5 HISTOGRAM EQUALIZATION
    # --------------------------------------------------------

    print("P4.5 Histogram Equalization")

    equalized, cdf, mapping = (
        histogram_equalization_manual(gray1)
    )

    save_gray(
        OUTPUT_DIR / "P4" / "08_histogram_equalization.png",
        equalized
    )

    hist_eq = histogram_gray_manual(
        equalized
    )

    save_histogram_png(
        OUTPUT_DIR / "P4" / "09_histogram_after_equalization.png",
        hist_eq,
        "Histogram Setelah Equalization",
        normalized=False
    )

    save_histogram_csv(
        OUTPUT_DIR / "P4" / "09_histogram_after_equalization.csv",
        hist_eq
    )

    save_mapping_csv(
        OUTPUT_DIR / "P4" / "10_equalization_mapping.csv",
        cdf,
        mapping
    )

    # --------------------------------------------------------
    # SELESAI
    # --------------------------------------------------------

    print()
    print("==============================================")
    print("SEMUA PROSES P3 + P4 SELESAI")
    print("==============================================")
    print(f"Hasil P3 : {OUTPUT_DIR / 'P3'}")
    print(f"Hasil P4 : {OUTPUT_DIR / 'P4'}")
    print()
    print("Catatan:")
    print("- Dataset mentah tetap berada di folder Mulberry.")
    print("- SAMPLE_STEP hanya membuat working copy manual.")
    print("- Operasi citra tidak memakai OpenCV/NumPy/scikit-image.")
    print("- Pillow hanya dipakai untuk membaca/menyimpan gambar.")


if __name__ == "__main__":
    main()
