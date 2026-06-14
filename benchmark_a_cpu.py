"""
=============================================================
  BENCHMARK A: CPU BENCHMARK (Sorting Data)
  Dataset   : 100.000 | 1.000.000 | 5.000.000
  Algoritma : Quick Sort | Merge Sort | Built-in Sort
  Variabel  : Execution Time, CPU Usage, Throughput
=============================================================
"""

import time
import random
import gc
import psutil
import threading


class ResourceMonitor:
    def __init__(self, interval=0.1):
        self.interval = interval
        self._cpu_samples = []
        self._running = False
        self._thread = None

    def start(self):
        self._cpu_samples.clear()
        self._running = True
        self._thread = threading.Thread(target=self._collect, daemon=True)
        self._thread.start()

    def _collect(self):
        while self._running:
            val = psutil.cpu_percent(interval=self.interval)
            self._cpu_samples.append(val)

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)

    @property
    def avg_cpu(self):
        samples = [s for s in self._cpu_samples if s > 0]
        return sum(samples) / len(samples) if samples else 0.0


# ── QUICK SORT ITERATIF ─────────────────────────────────────
def quick_sort(arr):
    arr = arr.copy()
    stack = [(0, len(arr) - 1)]
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        p = i + 1
        stack.append((low, p - 1))
        stack.append((p + 1, high))
    return arr


# ── MERGE SORT ITERATIF ─────────────────────────────────────
def merge_sort(arr):
    arr = arr.copy()
    n = len(arr)
    width = 1
    while width < n:
        for i in range(0, n, 2 * width):
            left  = i
            mid   = min(i + width, n)
            right = min(i + 2 * width, n)
            merged = []
            l, r = left, mid
            while l < mid and r < right:
                if arr[l] <= arr[r]:
                    merged.append(arr[l]); l += 1
                else:
                    merged.append(arr[r]); r += 1
            merged.extend(arr[l:mid])
            merged.extend(arr[r:right])
            arr[left:right] = merged
        width *= 2
    return arr


# ── BENCHMARK RUNNER ────────────────────────────────────────
def run_sort(sort_fn, data):
    monitor = ResourceMonitor()
    monitor.start()
    start   = time.perf_counter()
    sort_fn(data)
    elapsed = time.perf_counter() - start
    monitor.stop()
    throughput = len(data) / elapsed if elapsed > 0 else 0
    return elapsed, monitor.avg_cpu, throughput


def run():
    print("\n" + "=" * 70)
    print("  BENCHMARK A: CPU BENCHMARK (Sorting Data)")
    print("=" * 70)
    print(f"  {'Dataset':<20} {'Algoritma':<15} {'Exec Time (s)':<16} {'CPU (%)':<12} {'Throughput'}")
    print("-" * 70)

    sizes   = [100_000, 1_000_000, 5_000_000]
    results = []

    for n in sizes:
        gc.collect()
        data  = [random.randint(0, 1_000_000) for _ in range(n)]
        label = f"{n:,} data"

        for nama, fn in [("Quick Sort", quick_sort), ("Merge Sort", merge_sort), ("Built-in Sort", lambda d: sorted(d))]:
            elapsed, cpu, tp = run_sort(fn, data)
            print(f"  {label:<20} {nama:<15} {elapsed:<16.4f} {cpu:<12.2f} {tp:,.0f}")
            results.append({
                "dataset":    label,
                "algoritma":  nama,
                "exec_time":  elapsed,
                "cpu_usage":  cpu,
                "throughput": tp,
                "skip":       False,
            })

        print("-" * 70)
        del data

    print("=" * 70)
    return results


if __name__ == "__main__":
    run()