#!/usr/bin/env python3

### Standard packages ###
from __future__ import annotations
from hashlib import sha256
from secrets import token_bytes

### Third-party packages ###
from pydantic import BaseModel


class BinaryLabel(BaseModel):
  """Wire label for binary garbled circuits (traditional Yao)"""

  label: bytes  # 128-bit random label

  @classmethod
  def random(cls) -> BinaryLabel:
    return cls(label=token_bytes(16))

  def __xor__(self, other: BinaryLabel) -> BinaryLabel:
    return BinaryLabel(label=bytes(a ^ b for a, b in zip(self.label, other.label)))

  def hash_with(self, *others: BinaryLabel) -> bytes:
    """Hash labels together for garbled table encryption"""
    hash_string = sha256()
    hash_string.update(self.label)
    for other in others:
      hash_string.update(other.label)
    return hash_string.digest()[:16]


__all__: tuple[str, ...] = ("BinaryLabel",)
