#!/usr/bin/env python3

### Standard packages ###
from enum import Enum


class GateType(Enum):
  AND = "AND"
  XOR = "XOR"
  OR = "OR"
  ADD = "ADD"  # Arithmetic
  MUL = "MUL"  # Arithmetic


__all__: tuple[str, ...] = ("GateType",)
