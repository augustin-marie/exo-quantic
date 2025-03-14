from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
import os
from dotenv import load_dotenv

def dummy_sampler(service):
    # Create empty circuit
    example_circuit = QuantumCircuit(2)
    example_circuit.measure_all()

    backend = service.least_busy(operational=True, simulator=False)

    sampler = Sampler(backend)

    job = sampler.run([example_circuit])
    print(f"job id: {job.job_id()}")
    result = job.result()
    print(result)


if __name__ == "__main__": 
    load_dotenv() 
    key = os.getenv("KEY")

    service = QiskitRuntimeService(channel="ibm_quantum", token=key)

    dummy_sampler(service)

