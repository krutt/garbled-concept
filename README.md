# Garbled Concept

## Argo-Style Arithmetic Garbled Circuits Proof of Concept

[![Bitcoin-only](https://img.shields.io/badge/bitcoin-only-FF9900?logo=bitcoin)](https://twentyone.world)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/krutt/garbled-concept/blob/master/LICENSE)
[![Fork](https://img.shields.io/badge/fork-zscole/crypto--poc--daily-beige?logo=github)](https://github.com/zscole/crypto-poc-daily)
[![Top](https://img.shields.io/github/languages/top/krutt/garbled-concept)](https://github.com/krutt/garbled-concept)
[![Languages](https://img.shields.io/github/languages/count/krutt/garbled-concept)](https://github.com/krutt/garbled-concept)
[![Size](https://img.shields.io/github/repo-size/krutt/garbled-concept)](https://github.com/krutt/garbled-concept)
[![Last commit](https://img.shields.io/github/last-commit/krutt/garbled-concept/master)](https://github.com/krutt/garbled-concept)

### Overview

A repository aimed at demonstrating core concepts behind **Argo**, a new garbled circuits scheme
by [Liam Eagen](https://github.com/Liam-Eagen) & [Ying Tong Lai](https://github.com/therealyingtong)
that enables thousandfold more efficient off-chain computation for BitVM-style contracts.

### Key Innovation

**Problem:** Traditional garbled circuits work over **binary circuits** (AND, XOR, and etc.) where
each operation operates on individual bits. For cryptographic operations like elliptic curve
point multiplication, this requires *millions* of binary gates.

[Argo](https://eprint.iacr.org/2026/049) introduces **arithmetic circuits** using a
homomorphic MAC that encodes circuit wires as Elliptic Curve points. A single arithmetic
gate can represent what previously required millions of binary gates.

### Mission Statement

This proof-of-concept originally created by [zak.eth](https://github.com/zscole) as part of
[Crypto POC Daily](https://github.com/zscole/crypto-poc-daily) aims to demonstrate three main points

1. **Binary 💥 Arithmetic Circuits**: Side-by-side comparison showing gate count difference
2. **Homomorphic EC-MAC**: Implementation of a MAC scheme where operations on MACs correspond
  to operations on the underlying values
3. **Simple Garbled Gate**: Demonstration of garbling and evaluating gates using both approaches

### Concepts at play

#### Garbled Circuits (Yao's Protocol)

Garbled circuits allow two parties to compute a function on their private inputs without revealing
those inputs. One party "garbles" (encrypts) a circuit, the other "evaluates" it.

#### Why Arithmetic Circuits Matter for Bitcoin

[BitVM](https://bitvm.org) uses garbled circuits for off-chain computation with on-chain
dispute resolution. The efficiency of the garbled circuit directly impacts:

- Challenge/response size in disputes
- Number of on-chain transactions needed
- Overall practicality of BitVM contracts

Argo's thousandfold improvement makes previously impractical BitVM applications feasible.

## Prerequisites

* [python](https://www.python.org) 3.10 and above - High-level general-purpose programming language
* [uv](https://docs.astral.sh/uv) - extremely fast Python package & project manager written in Rust

### Getting Started

The following guide walks through setting up your local working environment using `uv`
as Python version manager as well as Python package manager. If you do not have `uv`
installed, run the following command.

<details>
  <summary> Install using Homebrew (Darwin) </summary>

  ```sh
  brew install uv
  ```
</details>

<details>
  <summary> Install using standalone installer (Darwin and Linux) </summary>

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
</details>

Once you have `uv` installed, you can install any version of Python above version 3.10 for this
project. The following commands help you set up and activate a Python virtual environment where
`uv` can download project dependencies from the `PyPI` open-sourced registry defined under
`pyproject.toml` file.

<details>
  <summary> Set up environment and synchroniz project dependencies </summary>

  ```sh
  uv venv --python 3.13.5
  source .venv/bin/activate
  uv sync --dev
  ```
</details>

#### Demonstrate Feasibility

```bash
# Install dependencies
uv sync

# Run demo
demonstrate
```

#### Run benchmarks for Argo-style Garbled Circuits against Traditional (Binary) Garbled Circuits

```bash
# Install dependencies
uv sync

# Run benchmarks
benchmark
```

### Project structure

<details>
  <summary> Tree structure </summary>

  ```
  garbled-concept/
  │
  ├── src/garbled-concept/
  │   │
  │   ├── __init__.py
  │   ├── benchmark.py
  │   ├── demonstrate.py
  │   ├── ec_mac.py
  │   ├── garbled_circuit.py
  │   ├── models/
  │   │   │
  │   │   ├── __init__.py
  │   │   ├── argo_wire.py
  │   │   ├── benchmark_result.py
  │   │   ├── binary_garbled_gate.py
  │   │   ├── binary_label.py
  │   │   ├── binary_wire.py
  │   │   ├── ec_mac.py
  │   │   ├── gate_type.py
  │   │   └── point.py
  │   │ 
  │   └── parameters.py
  │
  └── tests
      ├── __init__.py
      └── *TODO*.py
  ```
</details>

### Appendix

- [BitVM](https://bitvm.org) - [:page_facing_up:](https://bitvm.org/bitvm.pdf)
- [Garbled Locks - Newsletter #369](https://bitcoinops.org/en/newsletters/2025/06/20/#improvements-to-bitvm-style-contracts)
- [Bitcoin Optech Newsletter #390](https://bitcoinops.org/en/newsletters/2026/01/30/)  
- [Glock: Garbled Locks for Bitcoin](https://eprint.iacr.org/2025/1485) -
  [:page_facing_up:](https://eprint.iacr.org/2025/1485.pdf)
- [Argo: A Garbled Circuits Scheme for 1000x More Efficient Off-Chain Computation](https://eprint.iacr.org/2026/049) -
  [:page_facing_up:](https://eprint.iacr.org/2026/049.pdf)
- [{ ideal } Group](https://github.com/idealgroup) - [:globe_with_meridians:](https://ideal.group)
  - [Liam Eagen](https://github.com/Liam-Eagen) -
    [𝕏](https://x.com/liameagen),
    [:gun:](https://eprint.iacr.org/2025/1485)
  - [Ying Tong Lai](https://github.com/therealyingtong) -
    [𝕏](https://x.com/therealyingtong),
    [:writing_hand:](https://therealyingtong.github.io)

## License

This project is licensed under the terms of the MIT license.
