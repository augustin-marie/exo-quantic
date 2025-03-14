###
# Test des 3 gates de base
#
# X (Not quantique) : Inverse l'état d'un qubit
# H (Hadamard) : créé une supperposition
#
# CNOT : Controlled-not
# si le qubit de controle es 0 => rien
# si le qubit de controle est 1 => X(NOT) est appliqué sur le deuxième qubit
###

from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.quantum_info import SparsePauliOp
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import EstimatorV2 as Estimator
import os
from dotenv import load_dotenv

def run(qc):
    print("Execution sur serveur")
    load_dotenv() 
    key = os.getenv("KEY")
    service = QiskitRuntimeService(channel="ibm_quantum", token=key)

    # Set up six different observables.
    observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
    observables = [SparsePauliOp(label) for label in observables_labels]

    try:
        backend = service.least_busy(simulator=False, operational=True)

        # Convert to an ISA circuit and layout-mapped observables.
        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)

        isa_circuit = pm.run(qc)
        print(isa_circuit.draw(idle_wires=False))

        estimator (isa_circuit, backend, observables)
    except Exception as e:
        print("Impossible d'exécuter sur IBM Quantum :", e)


def estimator (circuit, backend, observables):
    # Construct the Estimator instance.
 
    estimator = Estimator(mode=backend)
    estimator.options.resilience_level = 1
    estimator.options.default_shots = 5000
 
    mapped_observables = [
        observable.apply_layout(circuit.layout) for observable in observables
    ]
 
    # One pub, with one circuit to run against five different observables.
    job = estimator.run([(circuit, mapped_observables)])
 
    # Use the job ID to retrieve your job data later
    print(f">>> Job ID: {job.job_id()}")


def cir_1():
    qc = QuantumCircuit(2)
    # Add a Hadamard gate to qubit 0
    qc.h(0)
    # Perform a controlled-X gate on qubit 1, controlled by qubit 0
    qc.cx(0, 1)

    print(qc.draw())
    
    return qc


if __name__ == "__main__":
    print("launching main function")
    # Circuit 1
    run(cir_1())
    

