from threading import Thread
from pod import Pod
from queue import Queue
import random
import time

class ProdutorPods(Thread):

    fila_de_pods: Queue
    n_pods = int

    def __init__(self, fila_de_pods: Queue, n_pods):
        super().__init__()

        self.fila_de_pods = fila_de_pods
        self.n_pods = n_pods

    def __str__(self):
        return (f"[Produtor de Pods]\n"
                f"Fila de pods: {str(self.fila_de_pods)}")
    
    def gerar_pod(self, id):
        #Valores possíveis de CPU, mem e disk
        valores_cpu = [1,2]
        valores_mem = [0.5,1,2,4]
        valores_disk = [5,10,20,40,50]

        cpu = random.choice(valores_cpu)
        mem = random.choice(valores_mem)
        disk = random.choice(valores_disk)

        return Pod(id,cpu,mem,disk)
    
    def run(self):
        print("[PRODUTOR] Produtor de pods iniciando...")
        time.sleep(3)

        for n in range(self.n_pods):
            pod = self.gerar_pod(n+1)
            self.fila_de_pods.put(pod)
            print(f"[PRODUTOR] Pod {pod.id} adicionado à fila.\n"
                  f"├── {str(pod)}")
            time.sleep(0.5)

        self.fila_de_pods.put(None)
        print("[PRODUTOR] Produção encerrada.")