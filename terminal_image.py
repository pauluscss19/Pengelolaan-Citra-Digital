"""
terminal_image.py

File utilitas (pembantu) ini berfungsi untuk mengubah hasil perhitungan matriks (citra) manual
menjadi file gambar sungguhan (.png) dan otomatis menyimpannya ke dalam folder 'Hasil'.
Semua fungsi tampilan terminal telah dihapus agar terminal lebih bersih.
"""

# Import modul 'os' untuk berinteraksi dengan sistem operasi (walau saat ini jarang dipakai di file ini).
import os

# Import 'Path' dari library 'pathlib' untuk mempermudah manipulasi jalur (path) folder dan file lintas OS.
from pathlib import Path

# Import 'inspect' untuk melacak (menginspeksi) asal usul kode. Kita pakai ini untuk tahu script mana yang memanggil fungsi ini.
import inspect

# Import 'Image' dari library 'PIL' (Pillow) yang bertugas secara spesifik membuat dan menyimpan gambar (bukan untuk menghitung algoritmanya).
from PIL import Image


def save_matrix_as_image(matrix, title, is_rgb=False):
    """
    Fungsi ini bertugas menerima matriks (array 2D) hasil perhitungan manual,
    lalu menyimpannya sebagai file PNG ke dalam folder 'Hasil'.
    """
    try:
        # Nilai default nama file jika tidak ditemukan siapa yang memanggilnya.
        caller_name = "output"
        # Nilai default folder adalah folder tempat terminal aktif saat ini.
        base_dir = Path.cwd()
        
        # inspect.stack() akan memberikan daftar urutan eksekusi file.
        # Kita melakukan perulangan (loop) untuk mencari tahu siapa yang memanggil utilitas ini.
        for frame_info in inspect.stack():
            # Jika nama filenya BUKAN 'terminal_image.py', berarti itu adalah script praktikumnya (misal: 01_Thresholding.py)
            if "terminal_image.py" not in frame_info.filename:
                # Ambil jalur lengkap file pemanggil tersebut.
                caller_path = Path(frame_info.filename)
                # Ambil nama filenya saja tanpa ekstensi (contoh: 01_Thresholding.py -> 01_Thresholding)
                caller_name = caller_path.stem
                # Ambil folder tempat file pemanggil itu berada.
                base_dir = caller_path.parent
                # Hentikan pencarian (keluar dari loop) karena script pemanggil sudah ditemukan.
                break
    except Exception:
        # Jika terjadi error saat mencari nama pemanggil, gunakan nilai default.
        caller_name = "output"
        base_dir = Path.cwd()

    # Gabungkan lokasi folder pemanggil dengan nama folder "Hasil"
    hasil_dir = base_dir / "Hasil"
    
    # Buat foldernya jika belum ada. exist_ok=True berarti tidak akan error jika foldernya sudah ada sebelumnya.
    hasil_dir.mkdir(exist_ok=True)

    # Membersihkan judul gambar dari karakter aneh agar aman dijadikan nama file.
    # Jika karakternya huruf/angka (isalnum) atau spasi/strip/underscore, biarkan. Selain itu ganti jadi underscore "_".
    safe_title = "".join(c if c.isalnum() or c in " _-" else "_" for c in title).strip("_").replace(" ", "_")
    
    # Buat format nama file dengan menggabungkan nama script pemanggil dan judul gambarnya. (contoh: 01_Thresholding_BEFORE_GRAYSCALE.png)
    filename = f"{caller_name}_{safe_title}.png"
    
    # Gabungkan folder Hasil dengan nama filenya menjadi satu jalur (path) utuh.
    out_path = hasil_dir / filename

    # Hitung tinggi gambar (jumlah baris matriks)
    height = len(matrix)
    # Hitung lebar gambar (jumlah kolom pada baris pertama matriks)
    width = len(matrix[0])

    # Tentukan mode gambar. "RGB" jika berwarna, atau "L" (Luminance) jika grayscale.
    mode = "RGB" if is_rgb else "L"
    
    # Buat canvas gambar baru yang kosong dengan ukuran dan mode yang telah ditentukan.
    img = Image.new(mode, (width, height))
    
    # Muat memori piksel dari gambar tersebut agar kita bisa mengubah warnanya satu-satu.
    pixels = img.load()

    # Looping vertikal (baris/Tinggi/Y)
    for y in range(height):
        # Looping horizontal (kolom/Lebar/X)
        for x in range(width):
            if is_rgb:
                # Jika gambar berwarna, ambil nilai R, G, B dan pastikan diubah menjadi integer (angka bulat) dalam format tuple (R, G, B)
                pixels[x, y] = tuple(int(v) for v in matrix[y][x])
            else:
                # Jika gambar grayscale, langsung ubah nilai matriks menjadi integer dan masukkan ke piksel.
                pixels[x, y] = int(matrix[y][x])

    # Setelah semua piksel selesai dimasukkan, simpan (save) gambar tersebut ke jalur path yang sudah dibuat sebelumnya.
    img.save(out_path)
    
    # Cetak pesan sukses ke terminal agar Anda tahu file sudah berhasil disimpan.
    print(f"[Simpan] {filename} tersimpan di folder Hasil/")


def draw_histogram_manual(hist, height=200):
    """
    Fungsi ini menggambar grafik batang histogram secara manual.
    Hasilnya berupa matriks (kanvas putih dengan garis hitam) 
    yang nantinya dapat disimpan sebagai gambar .png
    """
    # Buat matriks kanvas putih (255) berukuran 256 (lebar) x height (tinggi)
    graph = [[255 for _ in range(256)] for _ in range(height)]
    
    # Cari nilai frekuensi tertinggi untuk mengatur skala (tinggi maksimal)
    max_freq = 0
    for h in hist:
        if h > max_freq:
            max_freq = h
            
    if max_freq == 0:
        return graph
        
    for x in range(256):
        # Hitung tinggi baris (bar) untuk intensitas x secara proporsional
        bar_h = int((hist[x] / max_freq) * height)
        # Gambar garis hitam (0) dari bawah ke atas
        for y in range(height - 1, height - 1 - bar_h, -1):
            if y >= 0:
                graph[y][x] = 0
                
    return graph


def print_grayscale_before_after(
    before,
    after,
    before_title="BEFORE - ORIGINAL",
    after_title="AFTER",
    width=180,
    save_to_file=True
):
    """
    Fungsi ini sebelumnya untuk mencetak gambar grayscale ke terminal (sekarang diganti).
    Tugasnya saat ini HANYA meneruskan matriks grayscale untuk disimpan menjadi file PNG.
    """
    # Mengecek apakah variabel save_to_file bernilai True
    if save_to_file:
        # Simpan matriks 'before' (sebelum proses) menggunakan fungsi save_matrix_as_image (parameter is_rgb=False karena ini grayscale)
        save_matrix_as_image(before, before_title, is_rgb=False)
        # Simpan matriks 'after' (sesudah proses) menggunakan fungsi yang sama
        save_matrix_as_image(after, after_title, is_rgb=False)


def print_rgb_before_after(
    before_rgb,
    after_rgb,
    before_title="BEFORE - RGB",
    after_title="AFTER",
    width=180
):
    """
    Fungsi ini dipanggil oleh script praktikum yang mengolah gambar RGB (berwarna).
    Tugasnya langsung menyimpan gambar warna 'before' dan 'after' ke dalam format PNG.
    """
    # Simpan matriks 'before' yang berwarna dengan mengaktifkan is_rgb=True
    save_matrix_as_image(before_rgb, before_title, is_rgb=True)
    # Simpan matriks 'after' yang berwarna dengan is_rgb=True
    save_matrix_as_image(after_rgb, after_title, is_rgb=True)
