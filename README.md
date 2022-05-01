# quantum-information-stuff
Bunch of quantum information/computing projects/notes for personal learning usage

## What is this project about?
This repo consists the software packages for my undergraduate thesis project on quantum computation. 
In this project, I am building an optimization engine for the measurement-based quantum computational(MBQC) model.
The engine does the following optimization procedure while compiling a unitary circuit model to a MBQC model.
- It maps the algorithm expressed in unitary circuit into a MBQC model on cluster state
- It performs graph-based transformations to simulate the Clifford operations on the cluster state.
- It performs local complementation operations to search for an optimized graph state geometry.
- It conducts a measurement sequence where the memory efficiency is maximized.


[//]: # (and see if can provide a cheaper resource requirement compare to the unitary circuit implementation. )

[//]: # (I only have the engine and my algorithms still need polishment at the moment, )

[//]: # (but I think it is reasonable to actually make a compiler translate the unitary )

[//]: # (circuit language to measurement-based language and do optimizations on it.)

## What is the motivation?
Though quantum computation in general demonstrates advantages compare to classical computation,
A number of gates falls into the Clifford gate set can be efficiently simulated on classical computers.
Measurement calculus is a specific kind of graph-based simulation paradigm. 
It maps unitary gates into projective measurements on graph states and performs graph-based transformations to simulate the Clifford gates.
After the simulation, it maps the residual projective measurements back onto unitary gates no unitary circuit.


## Unitary circuit to MBQC
Please refer to `./graphoptim/experiments/DemoMBQC.py` for the use of `ClusterState`.

## TODO:
- [ ] Write documentations
- [ ] Remove redundency
