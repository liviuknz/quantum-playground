"""
Quantum Random Number Generator
===============================
Real randomness straight from quantum superposition. Each qubit is put into an
equal superposition with a Hadamard gate; measuring it collapses to 0 or 1 with
exactly 50/50 probability. The randomness is rooted in physics, not in a
deterministic pseudo-random algorithm.
"""
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

_SIM = AerSimulator()


def random_bits(n_bits: int) -> str:
    """Return n_bits truly-random bits from n_bits qubits in superposition."""
    qc = QuantumCircuit(n_bits, n_bits)
    qc.h(range(n_bits))                       # |0> -> (|0> + |1>) / sqrt(2)
    qc.measure(range(n_bits), range(n_bits))
    result = _SIM.run(transpile(qc, _SIM), shots=1).result()
    return next(iter(result.get_counts()))    # one shot -> one outcome


def random_int(low: int, high: int) -> int:
    """Random integer in [low, high] via rejection sampling on quantum bits."""
    span = high - low
    n_bits = max(1, span.bit_length())
    while True:
        value = int(random_bits(n_bits), 2)
        if value <= span:
            return low + value


if __name__ == "__main__":
    print("8 random quantum bits :", random_bits(8))
    print("Dice roll (1-6)       :", random_int(1, 6))
    print("Random byte (0-255)   :", random_int(0, 255))
