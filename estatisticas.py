from worker import Worker
from pod import Pod

def imprimir_tabela_workers(workers: list[Worker], titulo: str):
    """Imprime tabela de ocupação dos workers no terminal."""
    print(f"\n{'='*65}")
    print(f"  {titulo}")
    print(f"{'='*65}")
    print(f"  {'Worker':<10} {'CPU us/tot':>12} {'Mem us/tot':>12} {'Disk us/tot':>13} {'Ocup%':>7} {'PODs':>6}")
    print(f"  {'-'*60}")

    for w in workers:
        cpu_usado = w.cpu_total - w.cpu_disponivel
        mem_usado = w.mem_total - w.mem_disponivel
        disk_usado = w.disk_total - w.disk_disponivel

        print(f"  Worker {w.id:<4}"
              f"{cpu_usado:>4}/{w.cpu_total:<7}"
              f"{mem_usado:>4}/{w.mem_total:<7}GB"
              f"{disk_usado:>5}/{w.disk_total:<6}GB"
              f"{w.ocupacao_media():>6}%"
              f"{len(w.pods_alocados):>6}")

    print(f"{'='*65}")


def imprimir_tabela_pods(pods: list[Pod], titulo: str):
    """Imprime tabela de status de todos os pods."""
    print(f"\n{'='*65}")
    print(f"  {titulo}")
    print(f"{'='*65}")
    print(f"  {'POD':<10} {'CPU':>5} {'Mem':>6} {'Disk':>6} {'Status':<12} {'Worker':>8}")
    print(f"  {'-'*55}")

    for pod in pods:
        print(f"  POD {pod.id:<6}"
              f"{pod.cpu:>5}"
              f"{pod.mem:>5}GB"
              f"{pod.disk:>5}GB"
              f"  {pod.status:<12}"
              f"{str(pod.worker_id) if pod.worker_id else '-':>8}")

    print(f"{'='*65}")


def imprimir_resumo(pods: list[Pod], workers: list[Worker], titulo: str):
    """Imprime painel de estatísticas resumidas."""
    alocados = [p for p in pods if p.status == "Alocado"]
    rejeitados = [p for p in pods if p.status == "Rejeitado"]
    total = len(pods)

    ocup_media = sum(w.ocupacao_media() for w in workers) / len(workers)
    ocup_max = max(w.ocupacao_media() for w in workers)
    ocup_min = min(w.ocupacao_media() for w in workers)
    desequil = ocup_max - ocup_min

    print(f"\n{'='*65}")
    print(f"  ESTATÍSTICAS — {titulo}")
    print(f"{'='*65}")
    print(f"  PODs alocados   : {len(alocados)}/{total}")
    print(f"  PODs rejeitados : {len(rejeitados)}/{total}")
    print(f"  Taxa de sucesso : {len(alocados)/total*100:.1f}%")
    print(f"  Ocupação média  : {ocup_media:.1f}%")
    print(f"  Ocupação máxima : {ocup_max:.1f}%")
    print(f"  Ocupação mínima : {ocup_min:.1f}%")
    print(f"  Desequilíbrio   : {desequil:.1f}% ")
    print(f"{'='*65}")