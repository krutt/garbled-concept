#!/usr/bin/env python3

### Third-party packages ###
from pydantic import BaseModel, StrictFloat, StrictInt, StrictStr


class BenchmarkResult(BaseModel):
  name: StrictStr
  operations: StrictInt
  total_time_ms: StrictFloat
  per_op_ms: StrictFloat

  def __repr__(self):
    return f"{self.name}: {self.per_op_ms:.4f} ms/op ({self.operations} ops, {self.total_time_ms:.2f} ms total)"


__all__: tuple[str, ...] = ("BenchmarkResult",)
