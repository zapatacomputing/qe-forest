# qe-forest

[![codecov](https://codecov.io/gh/zapatacomputing/qe-forest/branch/main/graph/badge.svg?token=GI5NIW5TGI)](https://codecov.io/gh/zapatacomputing/qe-forest)

An Orquestra Quantum Engine Resource for Rigetti's Forest

## Overview

`qe-forest` is a Python module that exposes Rigetti's [Quantum Virtual Machine (QVM)](https://github.com/rigetti/qvm) simulator and [QUILC compiler](https://github.com/rigetti/quilc) as a [`z-quantum-core`](https://github.com/zapatacomputing/z-quantum-core/blob/main/src/python/zquantum/core/interfaces/backend.py) `QuantumSimulator`. In addition, it also provides converters that allow switching between [PyQuil](https://github.com/rigetti/pyquil) circuits and those of `z-quantum-core`.
It can be used directly in Python or in an [Orquestra](https://www.orquestra.io) workflow.
For more details, see the [Orquestra Pyquil integration docs](http://docs.orquestra.io/other-resources/framework-integrations/pyquil/).

For more information regarding Orquestra and resources, please refer to the [Orquestra documentation](https://www.orquestra.io/docs).

## Installation

This repository can be installed using `pip`. Clone the repository, enter the main directory of qe-forest, and run `pip install -e .`. For development install, run `pip install -e '.[dev]'` instead.

In order to run circuits using the QVM and QUILC we will need install the forest SDK. This process which is explained thoroughly in Rigetti's [getting started page](https://pyquil-docs.rigetti.com/en/stable/start.html?highlight=qvm) but we will go over it here for ease of use.

First, install [Rigetti's sdk](https://qcs.rigetti.com/sdk-downloads) making sure it has the necessary permissions. Once the install is completed, we will test is QVM and QUILC are working on your machine. Open 2 terminals, in one terminal run the command `qvm -S` and in the other run the command `quilc -S`. Some welcome text should appear, but you will not have the opportunity to input new commands to the terminals once these processes have started.

Finally, close the two previous terminals and open a third terminal. Navigate to the main directory of qe-forest and run `make test` to ensure your install was performed correctly. If all the tests pass then you're ready to use qe-forest!

## QVM and QUILC

For ease of use, qe-forest automatically starts QVM and QUILCS every time a ForestSimulator object is created so long as the ports 5000 an 5555 are free. If a ForestSimulator object is created while the ports for QVM or QUILC are being used, then a warning will be produced saying that a process is already running at the specified port. In principle, it is ok to make a new `ForestSimulator` while another is already using the ports. However, it is good practice to end the QVM and QUILC processes by running `simulator.kill_processes()` when you are done running a simulation.

## Development and contribution

You can find the development guidelines in the [`z-quantum-core` repository](https://github.com/zapatacomputing/z-quantum-core).
