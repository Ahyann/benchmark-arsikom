"""
=============================================================
  BENCHMARK D: STORAGE BENCHMARK (Baca / Tulis File)
  Dataset   : 100 MB | 1 GB | 5 GB
  Variabel  : Read Speed, Write Speed, Throughput
=============================================================
"""

import time
import os


CHUNK_SIZE = 4 * 1024 * 1024   # 4 MB per chunk
TMP_FILE   = "benchmark_tmp_storage.bin"


def run():
    print("\n" + "=" * 65)
    print("  BENCHMARK D: STORAGE BENCHMARK (Read / Write File)")
    print("=" * 65)
    print(f"  {'File Size':<15} {'Write Speed (MB/s)':<22} {'Read Speed (MB/s)':<22} {'Throughput (MB/s)'}")
    print("-" * 65)

    sizes_mb = [100, 1024, 5120]   # 100 MB, 1 GB, 5 GB
    results  = []
    chunk    = os.urandom(CHUNK_SIZE)

    for size_mb in sizes_mb:
        size_bytes = size_mb * 1024 * 1024
        label      = f"{size_mb} MB" if size_mb < 1024 else f"{size_mb // 1024} GB"

        # ── WRITE ──────────────────────────────────────
        written = 0
        start_w = time.perf_counter()
        with open(TMP_FILE, "wb") as f:
            while written < size_bytes:
                to_write = min(CHUNK_SIZE, size_bytes - written)
                f.write(chunk[:to_write])
                written += to_write
        elapsed_w   = time.perf_counter() - start_w
        write_speed = size_mb / elapsed_w if elapsed_w > 0 else 0

        # ── READ ───────────────────────────────────────
        start_r = time.perf_counter()
        with open(TMP_FILE, "rb") as f:
            while True:
                buf = f.read(CHUNK_SIZE)
                if not buf:
                    break
        elapsed_r  = time.perf_counter() - start_r
        read_speed = size_mb / elapsed_r if elapsed_r > 0 else 0

        throughput = (write_speed + read_speed) / 2

        print(f"  {label:<15} {write_speed:<22.2f} {read_speed:<22.2f} {throughput:.2f}")
        results.append({
            "dataset":     label,
            "write_speed": write_speed,
            "read_speed":  read_speed,
            "throughput":  throughput,
        })

        if os.path.exists(TMP_FILE):
            os.remove(TMP_FILE)

    print("=" * 65)
    return results


if __name__ == "__main__":
    run()