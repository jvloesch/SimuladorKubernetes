from worker import Worker
from pod import Pod
import copy

class MasterKubernetes:
    """
    Replica o comportamento padrão do Kubernetes:
    escalonamento usando apenas CPU e Memória (sem disco).
    Não usa threads. Roda de forma síncrona para comparação.
    """

    PESO_CPU = 0.5
    PESO_MEM = 0.5

    def __init__(self, workers_originais: list[Worker]):
        #Cria cópias zeradas dos mesmos workers para comparação justa
        self.workers = [
            Worker(w.id, w.cpu_total, w.mem_total, w.disk_total)
            for w in workers_originais
        ]
        self.todos_os_pods = []

    def calcular_score(self, worker):
        cpu_percent = worker.cpu_disponivel / worker.cpu_total
        mem_percent = worker.mem_disponivel / worker.mem_total

        return (
            cpu_percent * self.PESO_CPU +
            mem_percent * self.PESO_MEM
        )

    def escolher_melhor_worker(self, pod):
        melhor_worker = None
        melhor_score  = -1

        for worker in self.workers:
            if not worker.pode_alocar(pod):
                continue

            score = self.calcular_score(worker)

            if score > melhor_score:
                melhor_worker = worker
                melhor_score  = score

        return melhor_worker

    def escalonar(self, pod):
        worker = self.escolher_melhor_worker(pod)

        if worker is None:
            pod.status = "Rejeitado"
            return

        worker.alocar(pod)
        pod.status    = "Alocado"
        pod.worker_id = worker.id

    def escalonar_todos(self, pods_originais: list[Pod]):
        """
        Recebe a lista de pods já processados pelo Master e
        recria pods idênticos (sem estado) para rodar o scheduler padrão.
        """
        for pod_orig in pods_originais:
            pod = Pod(pod_orig.id, pod_orig.cpu, pod_orig.mem, pod_orig.disk)
            self.escalonar(pod)
            self.todos_os_pods.append(pod)
