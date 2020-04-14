# qe-forest

## What is it?


`qe-forest` is an [Orquestra](https://www.zapatacomputing.com/orquestra/) module that allows you to use Rigetti's [Quantum Virtual Machine (QVM)](https://github.com/rigetti/qvm) simulator and [QUILC compiler](https://github.com/rigetti/quilc) in your Orquestra workflows.
It complies to the backend interface defined in the [`z-quantum-core`](https://github.com/zapatacomputing/z-quantum-core/blob/master/src/python/orquestra/core/interfaces/backend.py).

## Usage

### Workflow
In order to use `qe-forest` in your workflow, you need to add it as a resource:

```yaml
resources:
- name: qe-forest
  type: git
  parameters:
    url: "git@github.com:zapatacomputing/qe-forest.git"
    branch: "master"
```

and then import in a specific step:

```yaml
- - name: my-task
    template: template-1
    arguments:
      parameters:
      - backend-specs: "{'module_name': 'qe.forest.simulator', 'function_name': 'ForestSimulator', 'device_name': 'wavefunction-simulator'}"
      - resources: [qe-forest]
```

You can pass additional arguments, such as `n_samples`, as parameters in the `backend-specs` dictionary. 

### Task

In order to use `QVM` the servers running `QVM` and `QUILC` must be started first. It needs to be done inside the task in the `artifacts` section:

```yaml
      artifacts:
      - name: main-script
        path: /app/main_script.sh
        raw:
          data: |
            qvm -S &
            quilc -S &
            python3 python_script.py
```

Then, in order to use backend in the python code we can either simply create an object:

```python
from qe.forest import ForestSimulator
backend = ForestSimulator()
```

or use `backend-specs` parameter to make our code work with other backends too:

```python
from zquantum.core.utils import create_object
backend_specs = {{inputs.parameters.backend-specs}}
backend = create_object(backend_specs)
```

## Development and contribution

You can find the development guidelines in the [`z-quantum-core` repository](https://github.com/zapatacomputing/z-quantum-core).
