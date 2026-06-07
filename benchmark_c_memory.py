"""
=============================================================
  BENCHMARK C: MEMORY BENCHMARK (Pencarian Data)
  Dataset   : 10 juta | 50 juta | 100 juta elemen
  Variabel  : RAM Usage, Execution Time
=============================================================
"""

import time
import random
import gc
import psutil


def get_ram_mb():
    return psutil.virtual_memory().used / (1024 ** 2)


def run():
    print("\n" + "=" * 65)
    print("  BENCHMARK C: MEMORY BENCHMARK (Data Search)")
    print("=" * 65)
    print(f"  {'Dataset':<22} {'RAM Used (MB)':<20} {'Exec Time (s)':<18} {'Found'}")
    print("-" * 65)

    sizes   = [10_000_000, 50_000_000, 100_000_000]
    results = []

    for n in sizes:
        gc.collect()
        time.sleep(0.5)  # beri jeda agar RAM stabil

        ram_before = get_ram_mb()

        # Buat data & langsung ukur RAM sesudahnya
        data      = list(range(n))
        ram_after_alloc = get_ram_mb()
        ram_used  = ram_after_alloc - ram_before

        target = random.randint(0, n - 1)

        start = time.perf_counter()
        found = target in data
        elapsed = time.perf_counter() - start

        label = f"{n // 1_000_000} juta elemen"
        print(f"  {label:<22} {ram_used:<20.2f} {elapsed:<18.6f} {found}")
        results.append({
            "dataset":   label,
            "ram_mb":    ram_used,
            "exec_time": elapsed,
            "found":     found,
        })
        del data
        gc.collect()

    print("=" * 65)
    return results


if __name__ == "__main__":
    run()