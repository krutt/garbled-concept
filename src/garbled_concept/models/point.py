#!/usr/bin/env python3

### Standard packages ###
from __future__ import annotations

### Third-party packages ###
from pydantic import BaseModel, StrictBool, StrictInt

### Local modules ###
from garbled_concept.parameters import Secp256k1


class Point(BaseModel):
  """Simple EC point representation"""

  x: StrictInt
  y: StrictInt
  is_infinity: StrictBool = False

  @classmethod
  def infinity(cls) -> Point:
    return cls(x=0, y=0, is_infinity=True)

  @classmethod
  def generator(cls) -> Point:
    return cls(x=Secp256k1.G_X, y=Secp256k1.G_Y)

  def __eq__(self, other: Point) -> bool:
    if self.is_infinity and other.is_infinity:
      return True
    return self.x == other.x and self.y == other.y

  def __repr__(self) -> str:
    if self.is_infinity:
      return "Point(∞)"
    return f"Point({hex(self.x)[:10]}..., {hex(self.y)[:10]}...)"


__all__: tuple[str, ...] = ("Point",)
