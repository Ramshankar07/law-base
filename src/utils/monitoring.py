from dataclasses import dataclass
from typing import Dict, List, Optional
import time


@dataclass
class PerformanceMetrics:
    execution_time: float
    memory_usage: float
    success_rate: float
    error_count: int


class PerformanceMonitor:
    def __init__(self):
        self.metrics: Dict[str, List[PerformanceMetrics]] = {}

    def start_operation(self, operation_name: str) -> float:
        return time.time()

    def end_operation(
        self,
        operation_name: str,
        start_time: float,
        success: bool = True,
        error: Optional[Exception] = None,
    ) -> None:
        execution_time = time.time() - start_time
        self.metrics.setdefault(operation_name, []).append(
            PerformanceMetrics(
                execution_time=execution_time,
                memory_usage=0.0,  # Implement memory tracking if needed
                success_rate=1.0 if success else 0.0,
                error_count=1 if error else 0,
            )
        )
