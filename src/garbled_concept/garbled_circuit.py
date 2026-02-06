#!/usr/bin/env python3
"""
Garbled Circuits: Binary vs Arithmetic

Demonstrates the fundamental difference between traditional binary garbled
circuits and Argo's arithmetic approach.
"""

### Standard packages ###
from __future__ import annotations

### Local modules ###
from garbled_concept.models import BinaryGarbledGate, BinaryWire, GateType


def count_binary_gates_for_multiplication(bits: int = 256) -> dict[str, int]:
  """
  Estimate gate count for a single EC point multiplication in binary circuits.

  A 256-bit modular multiplication requires:
  - ~256² AND gates for schoolbook multiplication
  - Plus XOR gates for addition/reduction
  - EC point multiplication needs ~256 of these plus point additions
  """

  # Schoolbook multiplication: n² AND gates, ~2n² XOR gates
  mul_and = bits * bits  # 65,536 AND gates per multiplication
  mul_xor = 2 * bits * bits  # 131,072 XOR gates

  # Modular reduction (simplified): ~2n² additional gates
  mod_gates = 2 * bits * bits

  # Single field multiplication
  field_mul_total = mul_and + mul_xor + mod_gates

  # EC point addition needs ~10 field multiplications + other ops
  ec_add_muls = 10
  ec_add_total = ec_add_muls * field_mul_total

  # Scalar multiplication (256-bit) needs ~384 point additions (on average)
  # Using double-and-add with ~50% bit density
  scalar_mul_point_ops = 384

  total_gates = scalar_mul_point_ops * ec_add_total

  return {
    "bits": bits,
    "single_field_mul_and": mul_and,
    "single_field_mul_xor": mul_xor,
    "single_field_mul_total": field_mul_total,
    "single_ec_add": ec_add_total,
    "total_scalar_mul_gates": total_gates,
    "total_millions": total_gates / 1_000_000,
  }


def count_arithmetic_gates_for_multiplication() -> dict[str, int]:
  """
  Gate count for EC point multiplication in Argo's arithmetic circuits.

  With arithmetic circuits over a prime field:
  - Field multiplication is a SINGLE arithmetic gate
  - EC point addition needs ~10 arithmetic gates
  - Scalar multiplication needs ~384 point operations
  """

  field_mul = 1  # Single gate!

  # EC point addition: ~10 field operations
  ec_add = 10

  # Scalar multiplication
  scalar_mul_point_ops = 384
  total = scalar_mul_point_ops * ec_add

  return {"single_field_mul": field_mul, "single_ec_add": ec_add, "total_scalar_mul_gates": total}


def compare_circuits():
  """Compare binary vs arithmetic circuit complexity"""
  print("=" * 70)
  print("Binary vs Arithmetic Garbled Circuits")
  print("=" * 70)

  print("\n--- Binary Circuit (Traditional Yao) ---")
  binary = count_binary_gates_for_multiplication()
  print("For a single 256-bit EC scalar multiplication:")
  print(f"  Single field multiplication: {binary['single_field_mul_total']:,} gates")
  print(f"    - AND gates: {binary['single_field_mul_and']:,}")
  print(f"    - XOR gates: {binary['single_field_mul_xor']:,}")
  print(f"  Single EC point addition: {binary['single_ec_add']:,} gates")
  print(f"  Full scalar multiplication: {binary['total_scalar_mul_gates']:,} gates")
  print(f"                            = {binary['total_millions']:.1f} million gates")

  print("\n--- Arithmetic Circuit (Argo) ---")
  arith = count_arithmetic_gates_for_multiplication()
  print("For a single 256-bit EC scalar multiplication:")
  print(f"  Single field multiplication: {arith['single_field_mul']} gate")
  print(f"  Single EC point addition: {arith['single_ec_add']} gates")
  print(f"  Full scalar multiplication: {arith['total_scalar_mul_gates']:,} gates")

  improvement = binary["total_scalar_mul_gates"] / arith["total_scalar_mul_gates"]
  print("\n--- Improvement ---")
  print(f"Argo is {improvement:,.0f}x more efficient for EC operations!")
  print("This is the '1000x improvement' mentioned in the paper.")

  return improvement


def demo_binary_garbled_gate():
  """Demonstrate a simple binary garbled AND gate"""
  print("\n" + "=" * 70)
  print("Binary Garbled AND Gate Demo")
  print("=" * 70)

  # Create wires
  wire_a = BinaryWire.create()
  wire_b = BinaryWire.create()
  wire_out = BinaryWire.create()

  # Garble the gate
  gate = BinaryGarbledGate(gate_type=GateType.AND, in_a=wire_a, in_b=wire_b, out=wire_out)

  print(f"\nGarbled table has {len(gate.garbled_table)} encrypted entries")
  print("Each entry is 16 bytes (128 bits)")

  # Evaluate with inputs (1, 1) -> should give 1
  a_val, b_val = 1, 1
  label_a = wire_a.get_label(a_val)
  label_b = wire_b.get_label(b_val)

  result_label = gate.evaluate(label_a, label_b)

  # Check which output value we got
  is_one = result_label.label == wire_out.label_1.label
  is_zero = result_label.label == wire_out.label_0.label

  print(f"\nInput: a={a_val}, b={b_val}")
  print(f"Expected AND result: {a_val & b_val}")
  print(f"Evaluator got label for: {'1' if is_one else '0' if is_zero else 'unknown'}")


if __name__ == "__main__":
  compare_circuits()
  demo_binary_garbled_gate()
