#!/usr/bin/env python3
"""
Elliptic Curve Homomorphic MAC - Argo Style

Demonstrates the core cryptographic primitive behind Argo:
A MAC scheme where the tag is an EC point, and operations on tags
correspond to arithmetic operations on the underlying values.

This enables arithmetic circuits over EC points rather than binary circuits.
"""

### Standard packages ###
from hashlib import sha256
from secrets import randbelow

### Local modules ###
from garbled_concept.models import ECMac, ECPoint
from garbled_concept.parameters import Secp256k1


def generate_h_point() -> ECPoint:
  """
  Generate a secondary generator H such that no one knows log_G(H).
  In practice, this is done via hash-to-curve.
  Here we use a simplified version.
  """
  # Hash a known string to get a deterministic "nothing up my sleeve" point
  h = sha256(b"argo-h-generator").digest()
  x = int.from_bytes(h, "big") % Secp256k1.P

  # Find a valid y for this x (simplified - in practice use proper hash-to-curve)
  # y^2 = x^3 + 7 (mod p)
  y_squared = (pow(x, 3, Secp256k1.P) + 7) % Secp256k1.P
  y = pow(y_squared, (Secp256k1.P + 1) // 4, Secp256k1.P)  # Tonelli-Shanks for p ≡ 3 (mod 4)

  if pow(y, 2, Secp256k1.P) != y_squared:
    # Try x+1 if first attempt fails
    x = (x + 1) % Secp256k1.P
    y_squared = (pow(x, 3, Secp256k1.P) + 7) % Secp256k1.P
    y = pow(y_squared, (Secp256k1.P + 1) // 4, Secp256k1.P)

  return ECPoint(x=x, y=y)


def demo_homomorphic_mac():
  """Demonstrate the homomorphic properties of the EC-MAC"""
  print("=" * 60)
  print("EC Homomorphic MAC Demonstration")
  print("=" * 60)

  H = generate_h_point()

  # Generate random keys
  k1 = randbelow(Secp256k1.N)
  k2 = randbelow(Secp256k1.N)

  # Values to compute on
  v1 = 42
  v2 = 100

  print(f"\nValues: v1 = {v1}, v2 = {v2}")

  # Create MACs
  mac1 = ECMac.create(k1, v1, H)
  mac2 = ECMac.create(k2, v2, H)

  print(f"\nMAC(k1, v1) = {mac1.tag}")
  print(f"MAC(k2, v2) = {mac2.tag}")

  # Homomorphic addition
  mac_sum = mac1.add(mac2)
  expected_sum = ECMac.create((k1 + k2) % Secp256k1.N, (v1 + v2) % Secp256k1.N, H)

  print("\n--- Homomorphic Addition ---")
  print(f"MAC(k1, v1) + MAC(k2, v2) = {mac_sum.tag}")
  print(f"MAC(k1+k2, v1+v2)         = {expected_sum.tag}")
  print(f"Match: {mac_sum.tag == expected_sum.tag}")

  # Homomorphic scalar multiplication
  c = 5
  mac_scaled = mac1.scalar_mul(c)
  expected_scaled = ECMac.create((c * k1) % Secp256k1.N, (c * v1) % Secp256k1.N, H)

  print("\n--- Homomorphic Scalar Multiplication ---")
  print(f"{c} * MAC(k1, v1)    = {mac_scaled.tag}")
  print(f"MAC({c}*k1, {c}*v1) = {expected_scaled.tag}")
  print(f"Match: {mac_scaled.tag == expected_scaled.tag}")

  return mac_sum.tag == expected_sum.tag and mac_scaled.tag == expected_scaled.tag


if __name__ == "__main__":
  success = demo_homomorphic_mac()
  print(f"\n{'✓ All checks passed!' if success else '✗ Some checks failed'}")
