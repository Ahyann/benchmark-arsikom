"""
=============================================================
  BENCHMARK A: CPU BENCHMARK (Sorting Data)
  Dataset   : 100.000 | 1.000.000 | 5.000.000
  Variabel  : Execution Time, CPU Usage, Throughput
=============================================================
"""

import time
import random
import gc
import psutil
import threading


class ResourceMonitor:
    def __init__(self, interval=0.2):
        self.interval = interval
        self._cpu_samples = []
        self._running = False
        self._thread = None

    def start(self):
        self._cpu_samples.clear()
        # warm-up agar pembacaan pertama tidak 0
        psutil.cpu_percent(interval=None)
        self._running = True
        self._thread = threading.Thread(target=self._collect, daemon=True)
        self._thread.start()

    def _collect(self):
        while self._running:
            val = psutil.cpu_percent(interval=self.interval)
            if val > 0:
                self._cpu_samples.append(val)

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)

    @property
    def avg_cpu(self):
        samples = [s for s in self._cpu_samples if s > 0]
        return sum(samples) / len(samples) if samples else 0.0


def run():
    print("\n" + "=" * 65)
    print("  BENCHMARK A: CPU BENCHMARK (Sorting Data)")
    print("=" * 65)
    print(f"  {'Dataset':<22} {'Exec Time (s)':<18} {'CPU Usage (%)':<18} {'Throughput (items/s)'}")
    print("-" * 65)

    sizes = [100_000, 1_000_000, 5_000_000]
    results = []

    for n in sizes:
        gc.collect()
        data = [random.randint(0, 10_000_000) for _ in range(n)]

        monitor = ResourceMonitor()
        monitor.start()
        start = time.perf_counter()
        data.sort()
        elapsed = time.perf_counter() - start
        monitor.stop()

        throughput = n / elapsed if elapsed > 0 else 0
        avg_cpu    = monitor.avg_cpu
        label      = f"{n:,} data"

        print(f"  {label:<22} {elapsed:<18.4f} {avg_cpu:<18.2f} {throughput:,.0f}")
        results.append({
            "dataset":    label,
            "exec_time":  elapsed,
            "cpu_usage":  avg_cpu,
            "throughput": throughput,
        })
        del data

    print("=" * 65)
    return results


if __name__ == "__main__":
    run()