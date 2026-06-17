"""
Deutsch-Jozsa Algorithm
=======================
A function f is promised to be either *constant* (same output for every input)
or *balanced* (0 for half the inputs, 1 for the rest). Classically you might
need up to 2^(n-1) + 1 queries to be certain. A quantum computer decides it with
a SINGLE query: measuring all-zeros means constant, anything else means balanced.
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

N = 3  # number of input qubits


def _oracle(qc: QuantumCircuit, kind: str) -> None:
    if kind == "constant":
        return                         # f(x) = 0 for all x -> do nothing
    for i in range(N):                 # balanced: f(x) = parity(x)
        qc.cx(i, N)


def deutsch_jozsa(kind: str = "balanced", shots: int = 1024) -> dict:
    qc = QuantumCircuit(N + 1, N)
    qc.x(N)                            # ancilla -> |1> for phase kickback
    qc.h(range(N + 1))
    _oracle(qc, kind)
    qc.h(range(N))                     # interfere the input register
    qc.measure(range(N), range(N))

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=shots).result().get_counts()


if __name__ == "__main__":
    for kind in ["constant", "balanced"]:
        counts = deutsch_jozsa(kind)
        measured = max(counts, key=counts.get)
        verdict = "constant" if measured == "0" * N else "balanced"
        flag = "OK" if verdict == kind else "MISMATCH"
        print(f"Oracle is {kind:9s} -> measured {measured} -> verdict: "
              f"{verdict}   [{flag}]")
