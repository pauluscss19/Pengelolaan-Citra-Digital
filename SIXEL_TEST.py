"""Tes minimal apakah terminal Windows pengguna merender SIXEL."""
import os
import tempfile
from pathlib import Path
import subprocess

# Persegi panjang putih 40 x 24 pixel pada latar terminal.
# Ini adalah stream SIXEL minimal, tanpa Pillow / OpenCV / NumPy.
sixel = (
    b"\x1bPq"
    b'"1;1;40;24'
    b"#1;2;100;100;100"
    b"!40~"
    b"-"
    b"#1!40~"
    b"-"
    b"#1!40~"
    b"-"
    b"#1!40~"
    b"\x1b\\"
)

fd, name = tempfile.mkstemp(prefix="sixel_test_", suffix=".sixel")
os.close(fd)
p = Path(name)
p.write_bytes(sixel)
print("Tes SIXEL: jika support aktif, akan muncul kotak putih kecil di atas.")
try:
    subprocess.run(["cmd.exe", "/d", "/c", "type", str(p)], check=True)
finally:
    p.unlink(missing_ok=True)
print("\nJika kotak tidak muncul, masalahnya ada pada terminal yang dipakai, bukan algoritma P3.")
