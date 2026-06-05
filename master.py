from threading import Thread
from worker import Worker
from pod import Pod
from queue import Queue
import random
import time

class Master(Thread):

    #Parâmetros (pesos) de escalonamento — 3 métricas
    PESO_CPU  = 0.5
    PESO_MEM  = 0.3
    PESO_DISK = 0.2

    workers: list[Worker]
    pods_pendentes: Queue
    n_workers: int

    def __init__(self, fila_de_pods: Queue, n_workers):
        super().__init__()

        self.pods_pendentes = fila_de_pods
        self.n_workers = n_workers
        self.workers = self.gerar_workers(self.n_workers)
        self.mostrar_workers()
        self.todos_os_pods = []  #histórico de todos os pods processados

    def __str__(self):
        return (f"[Master]\n"
                f"Pesos de escalonamento -> CPU: {self.PESO_CPU*100}%, "
                f"Memória: {self.PESO_MEM*100}%, "
                f"Disco: {self.PESO_DISK*100}%")

    def gerar_workers(self, n):
        valores_cpu  = [4, 8, 16]
        valores_mem  = [8, 16, 32, 64]
        valores_disk = [128, 256, 512]

        workers = []
        for i in range(n):
            cpu  = random.choice(valores_cpu)
            mem  = random.choice(valores_mem)
            disk = random.choice(valores_disk)
            workers.append(Worker(i + 1, cpu, mem, disk))

        return workers

    def mostrar_workers(self):
        for worker in self.workers:
            print(f"{worker}\n")

    def calcular_score(self, worker):
        cpu_percent  = worker.cpu_disponivel  / worker.cpu_total
        mem_percent  = worker.mem_disponivel  / worker.mem_total
        disk_percent = worker.disk_disponivel / worker.disk_total

        return (
            cpu_percent  * self.PESO_CPU  +
            mem_percent  * self.PESO_MEM  +
            disk_percent * self.PESO_DISK
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
            print(f"[MASTER] Nenhum worker disponível para o Pod {pod.id}")
            return

        worker.alocar(pod)
        pod.status    = "Alocado"
        pod.worker_id = worker.id

        print(f"[MASTER] Pod {pod.id} alocado ao Worker {worker.id}")

    def run(self):
        print("[MASTER] Master iniciando...")
        time.sleep(4)

        while True:
            pod = self.pods_pendentes.get()

            if pod is None:
                break

            print(f"[MASTER] Pod recebido: {pod.id}")
            self.escalonar(pod)
            self.todos_os_pods.append(pod)
            time.sleep(0.5)

        print("[MASTER] Escalonamento encerrado.")
        print("\n===== ESTADO FINAL DOS WORKERS =====")
        self.mostrar_workers()
