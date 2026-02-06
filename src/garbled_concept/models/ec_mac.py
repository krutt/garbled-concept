#!/usr/bin/env python3

### Standard packages ###
from __future__ import annotations

### Third-party packages ###
from pydantic import BaseModel

### Local modules ###
from garbled_concept.models.point import Point
from garbled_concept.parameters import Secp256k1


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
  if a == 0:
    return b, 0, 1
  gcd, x1, y1 = extended_gcd(b % a, a)
  x = y1 - (b // a) * x1
  y = x1
  return gcd, x, y


def mod_inverse(a: int, m: int) -> int:
  """Extended Euclidean algorithm for modular inverse"""
  if a < 0:
    a = a % m
  g, x, _ = extended_gcd(a, m)
  if g != 1:
    raise ValueError("Modular inverse does not exist")
  return x % m


def point_add(p1: Point, p2: Point) -> Point:
  """Add two EC points"""
  if p1.is_infinity:
    return p2
  if p2.is_infinity:
    return p1

  if p1.x == p2.x and p1.y != p2.y:
    return Point.infinity()

  if p1.x == p2.x:
    # Point doubling
    lam = (3 * p1.x * p1.x * mod_inverse(2 * p1.y, Secp256k1.P)) % Secp256k1.P
  else:
    # Point addition
    lam = ((p2.y - p1.y) * mod_inverse(p2.x - p1.x, Secp256k1.P)) % Secp256k1.P

  x3 = (lam * lam - p1.x - p2.x) % Secp256k1.P
  y3 = (lam * (p1.x - x3) - p1.y) % Secp256k1.P

  return Point(x=x3, y=y3)


def point_mul(k: int, p: Point) -> Point:
  """Scalar multiplication using double-and-add"""
  if k == 0:
    return Point.infinity()

  k = k % Secp256k1.N
  result = Point.infinity()
  addend = p

  while k:
    if k & 1:
      result = point_add(result, addend)
    addend = point_add(addend, addend)
    k >>= 1

  return result


class ECMac(BaseModel):
  """
  Elliptic Curve Homomorphic MAC

  The MAC of a value v with key k is: MAC(k, v) = k * G + v * H
  where G is the generator and H is a secondary generator.

  This MAC is additively homomorphic:
  MAC(k1, v1) + MAC(k2, v2) = MAC(k1+k2, v1+v2)

  And supports scalar multiplication:
  c * MAC(k, v) = MAC(c*k, c*v)
  """

  tag: Point

  @classmethod
  def create(cls, key: int, value: int, h_point: Point) -> ECMac:
    """Create a MAC for a value"""
    g_term = point_mul(key, Point.generator())
    h_term = point_mul(value, h_point)
    tag = point_add(g_term, h_term)
    return cls(tag=tag)

  def add(self, other: "ECMac") -> "ECMac":
    """Homomorphic addition"""
    new_tag = point_add(self.tag, other.tag)
    return ECMac(tag=new_tag)

  def scalar_mul(self, scalar: int) -> "ECMac":
    """Homomorphic scalar multiplication"""
    new_tag = point_mul(scalar, self.tag)
    return ECMac(tag=new_tag)


__all__: tuple[str, ...] = ("ECMac",)
