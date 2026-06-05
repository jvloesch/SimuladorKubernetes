from queue import Queue
from master import Master
from master_kubernetes import MasterKubernetes
from produtor_pods import ProdutorPods
from estatisticas import (imprimir_tabela_workers, imprimir_tabela_pods, imprimir_resumo)


def main():
    fila_de_pods = Queue()

    #Escalonador customizado (produtor/consumidor com threads)
    print("\n[INFO] Criando workers e iniciando Master customizado...\n")
    master = Master(fila_de_pods, n_workers=3)
    produtor = ProdutorPods(fila_de_pods, n_pods=20)

    master.start()
    produtor.start()

    produtor.join()
    master.join()

    #Exibe resultados do escalonador customizado
    imprimir_tabela_pods(master.todos_os_pods, titulo="PODs — Escalonador Customizado (CPU + Mem + Disk)")
    imprimir_tabela_workers(master.workers, titulo="Workers — Escalonador Customizado (CPU + Mem + Disk)")
    imprimir_resumo(master.todos_os_pods, master.workers, titulo="Escalonador Customizado")

    #Escalonador padrão do Kubernetes (CPU + Mem apenas)
    print("\n[INFO] Executando Escalonador Kubernetes padrão para comparação...")
    master_kub = MasterKubernetes(master.workers)
    master_kub.escalonar_todos(master.todos_os_pods)

    imprimir_tabela_pods(master_kub.todos_os_pods, titulo="PODs — Kubernetes Padrão (CPU + Mem)")
    imprimir_tabela_workers(master_kub.workers, titulo="Workers — Kubernetes Padrão (CPU + Mem)")
    imprimir_resumo(master_kub.todos_os_pods, master_kub.workers, titulo="Kubernetes Padrão")

    print("\nSimulação encerrada.")


if __name__ == "__main__":
    main()
