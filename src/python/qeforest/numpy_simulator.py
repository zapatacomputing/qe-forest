import os

import numpy as np
from zquantum.core.interfaces.backend import QuantumSimulator
from zquantum.core.measurement import ExpectationValues, Measurements, expectation_values_to_real
from pyquil import Program
from pyquil.pyqvm import PyQVM
from pyquil.wavefunction import Wavefunction
from pyquil.simulation._numpy import NumpyWavefunctionSimulator
from scipy.special import binom

class NumpySimulator(QuantumSimulator):
    def __init__(self, n_samples=None):
        self.n_samples = n_samples
    
    def run_circuit_and_measure(self, circuit, **kwargs):
        assert self.n_samples is not None
        wavefunction = self._get_wavefunction(circuit)
        n = len(circuit.qubits)
        bitstrings = [get_x_vec(i, n) for i in range(2**n)]
        probs = np.abs(wavefunction)**2
        rng = np.random.default_rng()
        samples = rng.choice(a=bitstrings, size=self.n_samples, p=probs)
        return Measurements(samples)

    def get_expectation_values(self, circuit, observable, **kwargs):
        if self.n_samples is None:
            return self.get_exact_expectation_values(circuit, observable, **kwargs)
        else:
            measurements = self.run_circuit_and_measure(circuit)
            expectation_values = measurements.get_expectation_values(observable)
            expectation_values = expectation_values_to_real(expectation_values)
            return expectation_values

    def get_exact_expectation_values(self, circuit, observable, **kwargs):
        wavefunction = self._get_wavefunction(circuit)
        probs = np.abs(wavefunction)**2
        n = len(circuit.qubits)
        bitstrings = [get_x_vec(i, n) for i in range(2**n)]
        expectation_values = []
        for term, coefficient in observable.terms.items():
            expectation = 0.0
            marked_qubits = [op[0] for op in term]
            for bitstring, prob in zip(bitstrings, probs):
                if sum([bitstring[i] for i in marked_qubits]) % 2 == 0:
                    expectation += probs
                else:
                    expectation -= probs
            expectation *= np.real(coefficient)
            expectation_values.append(np.real(expectation))
        return ExpectationValues(np.array(expectation_values))

#        eigenvalues = np.array(kwargs['eigenvalues'])
#        expectation_value = np.sum(eigenvalues*probs)
#        return ExpectationValues(np.array([expectation_value]))
        
    def get_exact_cvar(self, circuit, observable, **kwargs):
        wavefunction = self._get_wavefunction(circuit)
        probs = np.abs(wavefunction)**2

        alpha = kwargs['alpha']
        eigenvalues = kwargs['eigenvalues']
        ranks = kwargs['ranks']
        
        cumulative_prob = 0.0
        cumulative_value = 0.0
        
        for i in range(len(ranks)):
            j = ranks[i]
            if cumulative_prob + probs[j] < alpha:
                cumulative_prob += probs[j]
                cumulative_value += probs[j] * eigenvalues[j]
            else:
                cumulative_value += (alpha-cumulative_prob) * eigenvalues[j]
                cumulative_prob = alpha
                break
        cvar = cumulative_value / alpha
        return cvar
    
    def _get_wavefunction(self, circuit):
        n_qubits = len(circuit.qubits)
        qam = PyQVM(n_qubits=n_qubits, quantum_simulator_type=NumpyWavefunctionSimulator)
        
        program = Program()
        cnt = 0
        for gate in circuit.gates:
            if gate.name == "DICKE":
                assert cnt == 0
                k = gate.params[0]
                wf = np.zeros(2**n_qubits)
                for i in range(2**n_qubits):
                    x_vec = get_x_vec(i, n_qubits)
                    if sum(x_vec) == k:
                        wf[i] = 1.0
                wf /= np.sqrt(binom(n_qubits, k))
                wf = np.reshape(wf, [2]*n_qubits)
                qam.wf_simulator.wf = wf

            elif gate.name == "MPHASE":
                qam.execute(program)
                wf = qam.wf_simulator.wf
                reshaped_wf = np.reshape(wf, -1)

                assert len(gate.params) == len(reshaped_wf)
                phases = np.array(gate.params)
                reshaped_wf = reshaped_wf * phases

                wf = np.reshape(reshaped_wf, [2]*n_qubits)
                qam.wf_simulator.wf = wf
                program = Program()

            else:
                program += gate.to_pyquil()

            cnt += 1
                
        qam.execute(program)
        wf = qam.wf_simulator.wf
        reshaped_wf = np.reshape(wf, -1)
        return reshaped_wf

    def get_wavefunction(self, circuit):
        n = len(circuit.qubits)
        amplitudes = self._get_wavefunction(circuit)
        new_amplitudes = np.ones(2**n).astype(np.complex128)
        for i in range(2**n):
            b = format(i, 'b').zfill(n)
            rb = b[::-1]
            ri = int(rb, 2)
            new_amplitudes[ri] = amplitudes[i]
        return Wavefunction(new_amplitudes)
        
def get_x_vec(num, n):
    binary_string = format(num, 'b').zfill(n)
    return tuple(int(a) for a in binary_string)
