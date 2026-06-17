# 🧠⚛️ Quantum Playground

A small, hands-on collection of **quantum computing** demos written with
[Qiskit](https://www.ibm.com/quantum/qiskit). Each script is self-contained,
heavily commented, and actually runs on a local simulator — no quantum hardware
required.

> Four ideas that make quantum computing click: true randomness, entanglement,
> teleportation, and a real quantum speedup.

## What's inside

| File | Concept | The "wow" |
|------|---------|-----------|
| [`quantum_rng.py`](quantum_rng.py) | **Quantum RNG** | Randomness from physics — a qubit in superposition is a perfect coin flip. |
| [`bell_states.py`](bell_states.py) | **Entanglement** | Two qubits, always correlated: you see `00` or `11`, never `01`/`10`. |
| [`teleportation.py`](teleportation.py) | **Teleportation** | Move a qubit's state with 2 classical bits + 1 entangled pair, no cloning. |
| [`grover_search.py`](grover_search.py) | **Grover's search** | Find 1 item among 8 in ~√N steps — a quadratic quantum speedup. |

## Quick start

```bash
git clone https://github.com/liviuknz/quantum-playground.git
cd quantum-playground

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python quantum_rng.py
python bell_states.py
python teleportation.py
python grover_search.py
```

## Sample output

```text
$ python bell_states.py
Measurement results over 1024 shots:
  |00>:  508  #########################
  |11>:  516  #########################
Only 00 and 11 appear — the qubits are entangled.
```

```text
$ python grover_search.py
Secret item (qubit order q0q1q2): 101
Most-measured outcome:            101  (= qubit order 101)
```

## How it works (60-second tour)

- **Superposition** — a Hadamard gate (`h`) turns `|0⟩` into an equal blend of
  `|0⟩` and `|1⟩`. Measuring collapses it to a genuinely random bit.
- **Entanglement** — a Hadamard followed by a CNOT (`cx`) links two qubits so a
  measurement of one instantly determines the other.
- **Teleportation** — Alice's Bell measurement plus two classical bits let Bob
  rebuild the exact state she had, while her copy is destroyed (no-cloning).
- **Grover** — an *oracle* marks the answer with a phase flip and a *diffuser*
  amplifies it, so the right item dominates the measurement after ~√N rounds.

## Requirements

- Python 3.9+
- `qiskit` and `qiskit-aer` (see [`requirements.txt`](requirements.txt))

## License

[MIT](LICENSE) — use it, learn from it, build on it.
