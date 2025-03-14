from qiskit_ibm_runtime import QiskitRuntimeService
import os
from dotenv import load_dotenv
from matplotlib import pyplot as plt
 
###
# On récupérer le job après son execution pour faire les analyses et lectures de résultats
# Une variable d'env est ajoutée, JOB_ID, sa valeur est l'id renvoyé lors de l'exo 2
###

def recover():
    load_dotenv() 
    key = os.getenv("KEY")
    jobid = os.getenv("JOB_ID")

    service = QiskitRuntimeService(channel="ibm_quantum", token=key)
    
    return service.job(jobid)


def show_result(job):
    pub_result = job.result()[0]

    observables_labels = ["IZ", "IX", "ZI", "XI", "ZZ", "XX"]
    values = pub_result.data.evs
    errors = pub_result.data.stds

    plt.plot(observables_labels, values, "-o")
    plt.xlabel("Observables")
    plt.ylabel("Values")
    plt.show()


if __name__ == "__main__":
    job = recover()
    show_result(job)