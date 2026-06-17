"""
Grover's Search
===============
Find a "marked" item in an unsorted database of N items in about sqrt(N) steps
instead of N — a quadratic quantum speedup. Here we search 8 (= 2^3) items and
recover the secret one with high probability after just two iterations.
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def _ccz(qc: QuantumCircuit) -> None:
    """Controlled-controlled-Z on qubits 0,1 -> 2 (built from H + CCX)."""
    qc.h(2)
    qc.ccx(0, 1, 2)
    qc.h(2)


def _oracle(qc: QuantumCircuit, target: str) -> None:
    """Flip the phase of the basis state |target> (target[i] is qubit i)."""
    for i, bit in enumerate(target):
        if bit == "0":
            qc.x(i)
    _ccz(qc)
    for i, bit in enumerate(target):
        if bit == "0":
            qc.x(i)


def _diffuser(qc: QuantumCircuit) -> None:
    """Reflect the state about its average amplitude."""
    qc.h(range(3))
    qc.x(range(3))
    _ccz(qc)
    qc.x(range(3))
    qc.h(range(3))


def grover(target: str = "101", shots: int = 1024) -> dict:
    qc = QuantumCircuit(3, 3)
    qc.h(range(3))                 # uniform superposition over all 8 items
    for _ in range(2):             # optimal iteration count for N = 8
        _oracle(qc, target)
        _diffuser(qc)
    qc.measure(range(3), range(3))

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=shots).result().get_counts()


if __name__ == "__main__":
    target = "101"                 # qubit order q0 q1 q2
    counts = grover(target)
    winner = max(counts, key=counts.get)
    # Qiskit prints bitstrings as c2 c1 c0 (reversed vs qubit order)
    print(f"Secret item (qubit order q0q1q2): {target}")
    print(f"Most-measured outcome:            {winner}  "
          f"(= qubit order {winner[::-1]})")
    print("Full distribution:")
    for outcome, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {outcome}: {n:4d}  {'#' * (n // 20)}")
