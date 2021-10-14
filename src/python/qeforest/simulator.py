import errno
import socket
import subprocess

import numpy as np
from pyquil.api import WavefunctionSimulator, get_qc
from zquantum.core.circuits import Circuit
from zquantum.core.interfaces.backend import QuantumSimulator
from zquantum.core.wavefunction import flip_wavefunction, Wavefunction, flip_amplitudes
from zquantum.core.measurement import ExpectationValues, Measurements
from qeforest.conversions import export_to_pyquil, qubitop_to_pyquilpauli


class ForestSimulator(QuantumSimulator):
    supports_batching = False

    def __init__(self, device_name, seed=None, nthreads=1):
        super().__init__()
        self.nthreads = nthreads
        self.device_name = device_name
        self.seed = seed

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind(("127.0.0.1", 5000))
            subprocess.Popen(["qvm", "-S"])
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("QVM is already running")
            else:
                print(e)
        try:
            s.bind(("127.0.0.1", 5555))
            subprocess.Popen(["quilc", "-S"])
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                print("Quilc is already running")
            else:
                print(e)

        s.close()

    def run_circuit_and_measure(self, circuit, n_samples: int):
        """Run a circuit and measure a certain number of bitstrings. Note: the number
        of bitstrings measured is derived from self.n_samples

        Args:
            circuit: the circuit to prepare the state
            n_samples: The number of samples to measure.
        Returns:
            a list of bitstrings (a list of tuples)
        """
        super().run_circuit_and_measure(circuit, n_samples=n_samples)
        cxn = get_forest_connection(self.device_name, self.seed)
        bitstrings = cxn.run_and_measure(export_to_pyquil(circuit), trials=n_samples)
        if isinstance(bitstrings, dict):
            bitstrings = np.vstack([bitstrings[q] for q in sorted(cxn.qubits())]).T

        bitstrings = [tuple(b) for b in bitstrings.tolist()]
        return Measurements(bitstrings)

    def get_exact_expectation_values(self, circuit, qubit_operator):
        self.number_of_jobs_run += 1
        self.number_of_circuits_run += 1
        if self.device_name != "wavefunction-simulator":
            raise RuntimeError(
                "To compute exact expectation values, the device name must be "
                '"wavefunction-simulator". The device name is currently '
                f"{self.device_name}."
            )
        cxn = get_forest_connection(self.device_name, self.seed)

        # Pyquil does not support PauliSums with no terms.
        if len(qubit_operator.terms) == 0:
            return ExpectationValues(np.zeros((0,)))

        pauli_sum = qubitop_to_pyquilpauli(qubit_operator)
        expectation_values = np.real(
            cxn.expectation(export_to_pyquil(circuit), pauli_sum.terms)
        )

        if expectation_values.shape[0] != len(pauli_sum):
            raise (
                RuntimeError(
                    f"Expected {len(pauli_sum)} expectation values but received "
                    f"{expectation_values.shape[0]}."
                )
            )
        return ExpectationValues(expectation_values)

    def _get_wavefunction_from_native_circuit(self, circuit: Circuit, state):
        if not np.array_equal(state, [1] + [0] * (len(state) - 1)):
            raise ValueError(
                "ForestSimulator does not support starting simulations from state "
                "other than |0>. In particular, it currently does not support "
                "non-native circuit components."
            )

        cxn = get_forest_connection(self.device_name, self.seed)
        wavefunction = cxn.wavefunction(export_to_pyquil(circuit))
        return flip_amplitudes(wavefunction.amplitudes)


def get_forest_connection(device_name: str, seed=None):
    """Get a connection to a forest backend

    Args:
        device_name: the device to connect to

    Returns:
        A connection to either a pyquil simulator or a QPU
    """
    if device_name == "wavefunction-simulator":
        return WavefunctionSimulator(random_seed=seed)
    else:
        return get_qc(device_name)
