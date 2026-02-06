#!/usr/bin/env python3

### Third-party packages ###
from pydantic import Field, StrictInt
from pydantic_settings import BaseSettings


class EllipticCurve(BaseSettings):
  """
  Defaults use secp256k1 parameters (Bitcoin's curve)
  For simplicity, we work in a scalar field and simulate EC operations
  """

  P: StrictInt = Field(
    alias="CURVE_PRIME_MODULUS",
    default=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F,
    description="Prime modulus",
  )
  N: StrictInt = Field(
    alias="CURVE_ORDER",
    default=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141,
    description="Order; number of points on the curve that we can reach.",
  )
  G_X: StrictInt = Field(
    alias="CURVE_GENERATOR_X",
    default=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
    description="Generator point x-coordinate",
  )
  G_Y: StrictInt = Field(
    alias="CURVE_GENERATOR_Y",
    default=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8,
    description="Generator point y-coordinate",
  )


Secp256k1 = EllipticCurve()

__all__: tuple[str, ...] = ("EllipticCurve", "Secp256k1")
