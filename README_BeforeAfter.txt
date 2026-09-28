# P3 + P4 Mulberry - SIXEL Terminal

Versi FINAL.

Tujuan:
- setiap nomor P3/P4 tetap menjadi satu file terpisah,
- hasil gambar BEFORE/AFTER ditampilkan langsung sebagai grafik SIXEL,
- tidak menggunakan ASCII art,
- algoritma pengolahan citra tetap manual.

## Struktur folder yang wajib

C:\Users\ACER\pcd\
├── Mulberry\
│   ├── Healthy\
│   │   ├── healthy01.jpg
│   │   └── healthy02.jpg
│   ├── Leaf_Rust\
│   │   ├── rust01.jpg
│   │   └── rust02.jpg
│   └── Leaf_Spot\
│       ├── spot01.jpg
│       └── spot02.jpg
│
└── P3_P4_Mulberry_Sixel_FINAL\
    ├── terminal_image.py
    ├── P3_01_Thresholding.py
    ├── ...
    └── P4_05_Histogram_Equalization.py

Karena script membaca:
BASE_DIR = folder induk script
DATASET_DIR = BASE_DIR / "Mulberry"

maka file .py sebaiknya diletakkan satu folder di atasnya dengan folder
Mulberry pada level yang sama.

## Jika struktur Anda seperti ini

C:\Users\ACER\pcd\P3_P4_Mulberry_Sixel_FINAL\
    P3_01_Thresholding.py
    terminal_image.py
    Mulberry\
        Healthy\healthy01.jpg
        ...

maka path dataset sudah cocok juga.

## Install

pip install Pillow

Tidak membutuhkan:
- NumPy
- OpenCV
- SciPy
- scikit-image

Pillow hanya dipakai untuk membaca JPG/PNG.

## Menjalankan

PowerShell:

python .\P3_01_Thresholding.py

Lalu:
python .\P3_02_Negative.py

dan seterusnya.

## SIXEL

Program TIDAK menggambar piksel dengan ASCII atau blok Unicode.
Program mengirim stream SIXEL ke terminal.

Gunakan:
- Windows Terminal terbaru
- terminal yang mendukung SIXEL

Jika terminal tidak mendukung SIXEL, Anda dapat melihat karakter escape
atau gambar tidak muncul. Itu masalah kemampuan terminal, bukan algoritma.

## Manual

Pengolahan berikut ditulis manual:
- grayscale
- thresholding
- negative
- brightening
- arithmetic
- Boolean
- convolution
- translation
- rotation
- flipping
- scaling
- downsampling
- bilinear
- histogram
- normalisasi
- contrast stretching
- histogram equalization

Helper SIXEL hanya untuk DISPLAY.


PERBAIKAN VERSI FIXED2
- Tampilan SIXEL dikirim melalui `cmd.exe /d /c type` agar bytes grafik diteruskan mentah ke Windows Terminal.
- Jalankan `python SIXEL_TEST.py` untuk mengecek dukungan SIXEL.
- Jalankan skrip P3/P4 seperti biasa.
