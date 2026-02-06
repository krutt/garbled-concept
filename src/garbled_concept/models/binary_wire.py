#!/usr/bin/env python3

### Standard packages ###
from __future__ import annotations

### Third-party packages ###
from pydantic import BaseModel

### Local modules ###
from garbled_concept.models.binary_label import BinaryLabel


class BinaryWire(BaseModel):
  """A wire in a binary circuit with labels for 0 and 1"""

  label_0: BinaryLabel
  label_1: BinaryLabel

  @classmethod
  def create(cls) -> BinaryWire:
    return cls(label_0=BinaryLabel.random(), label_1=BinaryLabel.random())

  def get_label(self, value: int) -> BinaryLabel:
    return self.label_1 if value else self.label_0


__all__: tuple[str, ...] = ("BinaryWire",)
