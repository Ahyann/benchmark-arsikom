"""
=============================================================
  BENCHMARK B: FLOATING POINT BENCHMARK (Perkalian Matriks)
  Dataset   : 500x500 | 1000x1000 | 2000x2000
  Variabel  : Execution Time, CPU Usage, Memory Usage
=============================================================
"""

import time
import gc
import psutil
import threading
import numpy as np


class ResourceMonitor:
    def __init__(self, interval=0.1):
        self.interval = interval
        self._cpu_samples = []
        self._ram_samples = []
        self._running = False
        self._thread = None

    def start(self):
        self._cpu_samples.clear()
        self._ram_samples.clear()
        self._running = True
        self._thread = threading.Thread(target=self._collect, daemon=True)
        self._thread.start()

    def _collect(self):
        while self._running:
            # blocking call — tunggu interval lalu langsung dapat nilai
            val = psutil.cpu_percent(interval=self.interval)
            self._cpu_samples.append(val)
            self._ram_samples.append(psutil.virtual_memory().used / (1024 ** 2))

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)

    @property
    def avg_cpu(self):
        samples = [s for s in self._cpu_samples if s > 0]
        return sum(samples) / len(samples) if samples else 0.0

    @property
    def peak_ram_mb(self):
        return max(self._ram_samples) if self._ram_samples else 0.0

    @property
    def min_ram_mb(self):
        return min(self._ram_samples) if self._ram_samples else 0.0


def run():
    print("\n" + "=" * 65)
    print("  BENCHMARK B: FLOATING POINT (Matrix Multiplication)")
    print("=" * 65)
    print(f"  {'Matrix Size':<20} {'Exec Time (s)':<18} {'CPU Usage (%)':<18} {'Memory Used (MB)'}")
    print("-" * 65)

    sizes   = [500, 1000, 2000]
    results = []

    for n in sizes:
        gc.collect()
        time.sleep(0.3)

        ram_before = psutil.virtual_memory().used / (1024 ** 2)

        A = np.random.rand(n, n).astype(np.float64)
        B = np.random.rand(n, n).astype(np.float64)

        monitor = ResourceMonitor()
        monitor.start()
        start = time.perf_counter()
        C = np.dot(A, B)
        elapsed = time.perf_counter() - start
        monitor.stop()

        avg_cpu  = monitor.avg_cpu
        ram_used = max(monitor.peak_ram_mb - ram_before, 0)
        label    = f"{n}x{n}"

        print(f"  {label:<20} {elapsed:<18.4f} {avg_cpu:<18.2f} {ram_used:.2f}")
        results.append({
            "dataset":   label,
            "exec_time": elapsed,
            "cpu_usage": avg_cpu,
            "memory_mb": ram_used,
        })
        del A, B, C

    print("=" * 65)
    return results


if __name__ == "__main__":
    run()