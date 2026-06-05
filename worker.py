class Worker:

    id: str

    #Recursos totais (estáticos)
    cpu_total: int  #Cores
    mem_total: int  #RAM GB
    disk_total: int #GB

    #Recursos disponíveis (dinâmicos)
    cpu_disponivel: int  #Cores
    mem_disponivel: int  #RAM GB
    disk_disponivel: int #GB

    def __init__(self, id, cpu, mem, disk):
        self.id = id
        self.cpu_total = cpu
        self.mem_total = mem
        self.disk_total = disk

        self.cpu_disponivel = cpu
        self.mem_disponivel = mem
        self.disk_disponivel = disk

        self.pods_alocados = []  #Lista dos pods alocados neste worker

    def __str__(self):
        return (f"[Worker {self.id}]\n"
                f"  Totais -> CPU: {self.cpu_total}, Memória: {self.mem_total}GB, Disco: {self.disk_total}GB\n"
                f"  Disponível -> CPU: {self.cpu_disponivel}, Memória: {self.mem_disponivel}GB, Disco: {self.disk_disponivel}GB\n"
                f"  PODs -> {len(self.pods_alocados)} alocado(s)")

    def pode_alocar(self, pod):
        return (
            self.cpu_disponivel >= pod.cpu and
            self.mem_disponivel >= pod.mem and
            self.disk_disponivel >= pod.disk
        )

    def alocar(self, pod):
        self.cpu_disponivel  -= pod.cpu
        self.mem_disponivel  -= pod.mem
        self.disk_disponivel -= pod.disk
        self.pods_alocados.append(pod)

    def desalocar(self, pod):
        self.cpu_disponivel  += pod.cpu
        self.mem_disponivel  += pod.mem
        self.disk_disponivel += pod.disk
        self.pods_alocados.remove(pod)

    #Retorna o percentual médio de ocupação (CPU + Mem + Disk)
    def ocupacao_media(self):
        cpu_porcent  = (self.cpu_total - self.cpu_disponivel) / self.cpu_total * 100
        mem_porcent  = (self.mem_total - self.mem_disponivel) / self.mem_total * 100
        disk_porcent = (self.disk_total- self.disk_disponivel) / self.disk_total * 100
        return round((cpu_porcent + mem_porcent + disk_porcent) / 3, 1)
