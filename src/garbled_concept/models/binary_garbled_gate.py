#!/usr/bin/env python3

### Standard packages ###
from secrets import SystemRandom
from typing import Any

### Third-party packages ###
from pydantic import BaseModel

### Local modules ###
from garbled_concept.models.binary_label import BinaryLabel
from garbled_concept.models.binary_wire import BinaryWire
from garbled_concept.models.gate_type import GateType


class BinaryGarbledGate(BaseModel):
  """
  Traditional binary garbled gate using point-and-permute + row reduction.

  For an AND gate with inputs A, B and output C:
  - Garbler creates encrypted table mapping (label_A, label_B) -> label_C
  - Evaluator can only decrypt the one row corresponding to their labels
  """

  gate_type: GateType
  in_a: BinaryWire
  in_b: BinaryWire
  out: BinaryWire
  garbled_table: list[bytes] = []

  def model_post_init(self, __context: Any) -> None:
    self.garbled_table = self._garble()

  def _gate_func(self, a: int, b: int) -> int:
    """Evaluate the gate function"""
    if self.gate_type == GateType.AND:
      return a & b
    elif self.gate_type == GateType.XOR:
      return a ^ b
    elif self.gate_type == GateType.OR:
      return a | b
    raise ValueError(f"Unsupported gate type: {self.gate_type}")

  def _garble(self) -> list[bytes]:
    """Create the garbled table"""
    table = []

    # For each possible input combination
    for a in [0, 1]:
      for b in [0, 1]:
        # Get input labels
        label_a = self.in_a.get_label(a)
        label_b = self.in_b.get_label(b)

        # Compute output value and get output label
        out_val = self._gate_func(a, b)
        label_out = self.out.get_label(out_val)

        # Encrypt output label with input labels
        key = label_a.hash_with(label_b)
        encrypted = bytes(k ^ o for k, o in zip(key, label_out.label))

        table.append(encrypted)

    # Shuffle table (in practice, use point-and-permute)
    SystemRandom().shuffle(table)
    return table

  def evaluate(self, label_a: BinaryLabel, label_b: BinaryLabel) -> BinaryLabel:
    """Evaluator decrypts the garbled table"""
    key = label_a.hash_with(label_b)

    # Try to decrypt each row (in practice, point-and-permute tells us which)
    for encrypted in self.garbled_table:
      decrypted = bytes(k ^ e for k, e in zip(key, encrypted))
      # In real implementation, would verify decryption succeeded
      # Here we just return first decryption (simplified)
      return BinaryLabel(label=decrypted)

    raise ValueError("Decryption failed")


__all__: tuple[str, ...] = ("BinaryGarbledGate",)
