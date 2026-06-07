"""
=============================================================
  MAIN — UAS Arsitektur & Organisasi Komputer
  Jalankan file ini untuk menjalankan semua benchmark.
=============================================================
  Struktur file:
    main.py               ← file ini
    benchmark_a_cpu.py    ← CPU Benchmark (Sorting)
    benchmark_b_float.py  ← Floating Point (Matrix Multiply)
    benchmark_c_memory.py ← Memory Benchmark (Search)
    benchmark_d_storage.py← Storage Benchmark (Read/Write)
=============================================================
"""

import platform
import psutil
import benchmark_a_cpu
import benchmark_b_float
import benchmark_c_memory
import benchmark_d_storage


def print_system_info():
    print("\n" + "=" * 65)
    print("  SYSTEM INFORMATION")
    print("=" * 65)
    print(f"  OS           : {platform.system()} {platform.release()}")
    print(f"  Processor    : {platform.processor()}")
    print(f"  CPU Cores    : {psutil.cpu_count(logical=False)} Physical, "
          f"{psutil.cpu_count(logical=True)} Logical")
    mem = psutil.virtual_memory()
    print(f"  Total RAM    : {mem.total / (1024**3):.2f} GB")
    print(f"  Python       : {platform.python_version()}")
    print("=" * 65)


def print_summary(cpu_r, fp_r, mem_r, stor_r):
    print("\n\n" + "=" * 65)
    print("  RINGKASAN HASIL BENCHMARK")
    print("=" * 65)

    print("\n[A] CPU Benchmark (Sorting)")
    print(f"  {'Dataset':<22} {'Time (s)':<15} {'CPU (%)':<15} {'Throughput (items/s)'}")
    for r in cpu_r:
        print(f"  {r['dataset']:<22} {r['exec_time']:<15.4f} {r['cpu_usage']:<15.2f} {r['throughput']:,.0f}")

    print("\n[B] Floating Point (Matrix Multiply)")
    print(f"  {'Matrix':<20} {'Time (s)':<15} {'CPU (%)':<15} {'RAM (MB)'}")
    for r in fp_r:
        print(f"  {r['dataset']:<20} {r['exec_time']:<15.4f} {r['cpu_usage']:<15.2f} {r['memory_mb']:.2f}")

    print("\n[C] Memory Benchmark (Search)")
    print(f"  {'Dataset':<22} {'RAM (MB)':<15} {'Time (s)':<15} {'Found'}")
    for r in mem_r:
        print(f"  {r['dataset']:<22} {r['ram_mb']:<15.2f} {r['exec_time']:<15.6f} {r['found']}")

    print("\n[D] Storage Benchmark (Read/Write) — kecepatan dalam MB/s")
    print(f"  {'File Size':<15} {'Write (MB/s)':<20} {'Read (MB/s)':<20} {'Throughput'}")
    for r in stor_r:
        print(f"  {r['dataset']:<15} {r['write_speed']:<20.2f} {r['read_speed']:<20.2f} {r['throughput']:.2f} MB/s")

    print("\n" + "=" * 65)
    print("  Benchmark selesai! Screenshot hasil ini untuk laporan.")
    print("=" * 65 + "\n")


def main():
    print("=" * 65)
    print("  BENCHMARK PROGRAM — UAS ARSITEKTUR & ORGANISASI KOMPUTER")
    print("=" * 65)

    print_system_info()

    input("\nTekan ENTER untuk memulai semua benchmark...\n")

    print("\nMenunggu sebentar sebelum mulai...")

    cpu_results  = benchmark_a_cpu.run()
    fp_results   = benchmark_b_float.run()
    mem_results  = benchmark_c_memory.run()
    stor_results = benchmark_d_storage.run()

    print_summary(cpu_results, fp_results, mem_results, stor_results)


if __name__ == "__main__":
    main()