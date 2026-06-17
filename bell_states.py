"""
Bell State — Quantum Entanglement
=================================
Builds the maximally-entangled Bell pair (|00> + |11>) / sqrt(2). Measure both
qubits thousands of times and you only ever see 00 or 11 — never 01 or 10. The
two qubits are perfectly correlated regardless of the distance between them:
Einstein's "spooky action at a distance".
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def bell_pair(shots: int = 1024) -> dict:
    qc = QuantumCircuit(2, 2)
    qc.h(0)                 # put qubit 0 in superposition
    qc.cx(0, 1)             # entangle: qubit 1 now follows qubit 0
    qc.measure([0, 1], [0, 1])

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=shots).result().get_counts()


if __name__ == "__main__":
    counts = bell_pair()
    print("Measurement results over 1024 shots:")
    for outcome, n in sorted(counts.items()):
        print(f"  |{outcome}>: {n:4d}  {'#' * (n // 20)}")
    print("\nOnly 00 and 11 appear — the qubits are entangled.")
