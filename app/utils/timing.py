"""
Timing utility for precise latency measurement

Uses time.perf_counter() for high-resolution timing.
"""

import time

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start the timer"""
        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer and return latency in milliseconds"""
        if self._start_time is None:
            return 0.0
        
        end_time = time.perf_counter()
        latency = (end_time - self._start_time) * 1000
        return latency
