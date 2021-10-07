# qe-forest

[![codecov](https://codecov.io/gh/zapatacomputing/qe-forest/branch/master/graph/badge.svg?token=GI5NIW5TGI)](https://codecov.io/gh/zapatacomputing/qe-forest)

An Orquestra Quantum Engine Resource for Rigetti's Forest

## Overview

`qe-forest` is a Python module that exposes Rigetti's [Quantum Virtual Machine (QVM)](https://github.com/rigetti/qvm) simulator and [QUILC compiler](https://github.com/rigetti/quilc) as a [`z-quantum-core`](https://github.com/zapatacomputing/z-quantum-core/blob/master/src/python/zquantum/core/interfaces/backend.py) `QuantumSimulator`. In addition, it also provides converters that allow switching between [PyQuil](https://github.com/rigetti/pyquil) circuits and those of `z-quantum-core`.
It can be used directly in Python or in an [Orquestra](https://www.orquestra.io) workflow.
For more details, see the [Orquestra Pyquil integration docs](http://docs.orquestra.io/other-resources/framework-integrations/pyquil/).

For more information regarding Orquestra and resources, please refer to the [Orquestra documentation](https://www.orquestra.io/docs).

## Development and contribution

You can find the development guidelines in the [`z-quantum-core` repository](https://github.com/zapatacomputing/z-quantum-core).
