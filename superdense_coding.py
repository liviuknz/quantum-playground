"""
Superdense Coding
=================
The mirror image of teleportation: Alice sends TWO classical bits to Bob by
physically transmitting just ONE qubit, using a pre-shared entangled pair. She
encodes her two bits with one of {I, X, Z, ZX}; Bob decodes them with a CNOT
and a Hadamard.
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def superdense(message: str = "10", shots: int = 1024) -> dict:
    qc = QuantumCircuit(2, 2)

    # Shared Bell pair: qubit 0 stays with Alice, qubit 1 goes to Bob
    qc.h(0)
    qc.cx(0, 1)

    # Alice encodes two classical bits (b1 b0) onto her single qubit
    b1, b0 = message[0], message[1]
    if b0 == "1":
        qc.x(0)
    if b1 == "1":
        qc.z(0)

    # Alice sends her qubit to Bob, who decodes both bits
    qc.cx(0, 1)
    qc.h(0)
    qc.measure([0, 1], [0, 1])

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=shots).result().get_counts()


if __name__ == "__main__":
    for msg in ["00", "01", "10", "11"]:
        counts = superdense(msg)
        # Qiskit returns bits little-endian (q1 q0); reverse to read b1 b0
        decoded = max(counts, key=counts.get)[::-1]
        ok = "OK" if decoded == msg else "MISMATCH"
        print(f"Alice sent {msg} -> Bob decoded {decoded}   [{ok}]")
