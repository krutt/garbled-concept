#!/usr/bin/env python3

### Standard packages ###
from __future__ import annotations
from typing import Any

### Third-party packages ###
from pydantic import BaseModel

### Local modules ###
from garbled_concept.models.m_a_c import MAC
from garbled_concept.models.point import Point
from garbled_concept.parameters import Secp256k1


class ArgoWire(BaseModel):
  """
  Represents a wire in an Argo-style arithmetic circuit.

  Each wire carries a value v and its MAC: (v, MAC(k, v))
  The key k is known only to the garbler.
  """

  value: int
  mac: MAC
  h_point: Point

  def model_post_init(self, __context: Any) -> None:
    self.value = self.value % Secp256k1.N

  @classmethod
  def create(cls, value: int, key: int, h_point: Point) -> ArgoWire:
    """Create a new wire with a value and fresh MAC"""
    mac = MAC.create(key, value, h_point)
    return cls(value=value, mac=mac, h_point=h_point)

  def add(self, other: ArgoWire) -> ArgoWire:
    """
    Addition gate: output = input1 + input2

    The evaluator can compute this without knowing the key!
    (v1, MAC(k1, v1)) + (v2, MAC(k2, v2)) = (v1+v2, MAC(k1+k2, v1+v2))
    """
    new_value = (self.value + other.value) % Secp256k1.N
    new_mac = self.mac.add(other.mac)
    return ArgoWire(value=new_value, mac=new_mac, h_point=self.h_point)

  def mul_const(self, c: int) -> ArgoWire:
    """
    Multiplication by constant: output = c * input

    The evaluator can compute: c * (v, MAC(k, v)) = (c*v, MAC(c*k, c*v))
    """
    c = c % Secp256k1.N
    new_value = (c * self.value) % Secp256k1.N
    new_mac = self.mac.scalar_mul(c)
    return ArgoWire(value=new_value, mac=new_mac, h_point=self.h_point)

  def verify(self, key: int) -> bool:
    """Verify the MAC (garbler only)"""
    expected = MAC.create(key, self.value, self.h_point)
    return self.mac.tag == expected.tag


__all__: tuple[str, ...] = ("ArgoWire",)
