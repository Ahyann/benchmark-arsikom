# Benchmark UAS — Arsitektur & Organisasi Komputer

Program benchmark untuk mengukur dan membandingkan performa hardware dua komputer, mencakup CPU, Floating Point, Memory, dan Storage.

---

## Struktur File

```
benchmark/
├── main.py                 <- jalankan file ini
├── benchmark_a_cpu.py      <- CPU Benchmark (Sorting Data)
├── benchmark_b_float.py    <- Floating Point (Perkalian Matriks)
├── benchmark_c_memory.py   <- Memory Benchmark (Pencarian Data)
└── benchmark_d_storage.py  <- Storage Benchmark (Baca/Tulis File)
```

---

## Requirements

- Python 3.10+
- psutil
- numpy

---

## Cara Menjalankan

1. Clone repo ini

```bash
git clone https://github.com/Username/benchmark-arsikom.git
cd benchmark-arsikom
```

2. Install library

```bash
pip install psutil numpy
```

> Kalau muncul error `No module found`, coba:
> ```bash
> python -m pip install psutil numpy
> ```

3. Jalankan program

```bash
python main.py
```

4. Tekan ENTER saat diminta untuk memulai benchmark.

---

## Benchmark yang Diukur

**A. CPU Benchmark (Sorting Data)**
Dataset: 100.000 | 1.000.000 | 5.000.000 data
Variabel: Execution Time, CPU Usage, Throughput

**B. Floating Point (Perkalian Matriks)**
Dataset: 500x500 | 1000x1000 | 2000x2000
Variabel: Execution Time, CPU Usage, Memory Usage

**C. Memory Benchmark (Pencarian Data)**
Dataset: 10 juta | 50 juta | 100 juta elemen
Variabel: RAM Usage, Execution Time

**D. Storage Benchmark (Baca/Tulis File)**
Dataset: 100 MB | 1 GB | 5 GB
Variabel: Read Speed, Write Speed, Throughput

---

## Catatan

- Semua file `.py` harus berada dalam satu folder yang sama
- Benchmark C butuh RAM minimal 4 GB bebas
- Tutup aplikasi lain sebelum menjalankan agar hasil lebih akurat

---

## Kelompok

Ahyan Nubaid
Muhammad Fabian Rizky
Izadine Akhmad Zantika

Mata Kuliah: Arsitektur & Organisasi Komputer
Semester 2
