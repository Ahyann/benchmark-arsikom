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


# ── QUICK SORT ──────────────────────────────────────────────
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left  = [x for x in arr if x < pivot]
    mid   = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# ── MERGE SORT ──────────────────────────────────────────────
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid   = len(arr) // 2
    left  = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ── BENCHMARK RUNNER ────────────────────────────────────────
def run_sort(label, sort_fn, data):
    monitor = ResourceMonitor()
    monitor.start()
    start   = time.perf_counter()
    sort_fn(data.copy())
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

    # Quick Sort hanya sampai 1jt karena rekursi Python ada batasnya
    sizes = [100_000, 1_000_000, 5_000_000]
    results = []

    for n in sizes:
        gc.collect()
        data  = [random.randint(0, 1_000_000) for _ in range(n)]
        label = f"{n:,} data"

        # Quick Sort — skip 5 juta karena Python recursion limit
        if n <= 1_000_000:
            elapsed, cpu, tp = run_sort(label, quick_sort, data)
            print(f"  {label:<20} {'Quick Sort':<15} {elapsed:<16.4f} {cpu:<12.2f} {tp:,.0f}")
            results.append({"dataset": label, "algoritma": "Quick Sort", "exec_time": elapsed, "cpu_usage": cpu, "throughput": tp})
        else:
            print(f"  {label:<20} {'Quick Sort':<15} {'skip (recursion limit)':<16}")

        # Merge Sort — skip 5 juta karena Python recursion limit
        if n <= 1_000_000:
            elapsed, cpu, tp = run_sort(label, merge_sort, data)
            print(f"  {label:<20} {'Merge Sort':<15} {elapsed:<16.4f} {cpu:<12.2f} {tp:,.0f}")
            results.append({"dataset": label, "algoritma": "Merge Sort", "exec_time": elapsed, "cpu_usage": cpu, "throughput": tp})
        else:
            print(f"  {label:<20} {'Merge Sort':<15} {'skip (recursion limit)':<16}")

        # Built-in Sort — semua ukuran
        elapsed, cpu, tp = run_sort(label, lambda d: d.sort(), data)
        print(f"  {label:<20} {'Built-in Sort':<15} {elapsed:<16.4f} {cpu:<12.2f} {tp:,.0f}")
        results.append({"dataset": label, "algoritma": "Built-in", "exec_time": elapsed, "cpu_usage": cpu, "throughput": tp})

        print("-" * 70)
        del data

    print("=" * 70)
    return results


if __name__ == "__main__":
    run()