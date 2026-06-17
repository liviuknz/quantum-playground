"""
Quantum Teleportation
=====================
Transmit an unknown qubit state from Alice to Bob using one shared entangled
pair plus two classical bits — without ever moving the qubit itself. The
original state is destroyed on Alice's side (the no-cloning theorem holds) and
faithfully recreated on Bob's.

We verify success by un-preparing Bob's qubit at the end: if teleportation
worked, his verification bit reads 0 essentially 100% of the time.
"""
import math
from qiskit import (QuantumCircuit, QuantumRegister, ClassicalRegister,
                    transpile)
from qiskit_aer import AerSimulator


def teleport(theta: float = math.pi / 3, shots: int = 1024) -> dict:
    q = QuantumRegister(3, "q")        # q0 = payload, q1/q2 = entangled pair
    crz = ClassicalRegister(1, "crz")  # drives the Z correction
    crx = ClassicalRegister(1, "crx")  # drives the X correction
    out = ClassicalRegister(1, "out")  # verification readout on Bob's qubit
    qc = QuantumCircuit(q, crz, crx, out)

    # Alice prepares the (arbitrary) state she wants to send
    qc.ry(theta, 0)

    # Shared entangled pair: Alice holds q1, Bob holds q2
    qc.h(1)
    qc.cx(1, 2)

    # Alice entangles the payload with her half and measures both
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, crz)
    qc.measure(1, crx)

    # Bob's corrections, conditioned on Alice's two classical bits
    with qc.if_test((crx, 1)):
        qc.x(2)
    with qc.if_test((crz, 1)):
        qc.z(2)

    # Verify: undo the original preparation on Bob's qubit -> expect |0>
    qc.ry(-theta, 2)
    qc.measure(2, out)

    sim = AerSimulator()
    return sim.run(transpile(qc, sim), shots=shots).result().get_counts()


if __name__ == "__main__":
    counts = teleport()
    # result keys look like "out crx crz"; the leftmost token is Bob's readout
    bob_ok = sum(n for key, n in counts.items() if key.split()[0] == "0")
    total = sum(counts.values())
    print(f"Bob recovered the state in {bob_ok}/{total} shots "
          f"({100 * bob_ok / total:.1f}%).")
    print("A ~100% success rate means the qubit was teleported faithfully.")
