class Pod:

    id: str

    #Recursos que consome
    cpu: int #Cores
    mem: int #RAM GB
    disk: int #GB

    #Estado
    status: str #"Pendente", "Alocado", "Rejeitado"
    worker_id: str #ID do worker onde foi alocado (None se não alocado)

    def __init__(self, id, cpu, mem, disk):
        self.id = id
        self.cpu = cpu
        self.mem = mem
        self.disk = disk
        self.status = "Pendente"
        self.worker_id = None

    def __str__(self):
        return (f"[POD {self.id:02d}] "
                f"CPU: {self.cpu}, Mem: {self.mem}GB, Disco: {self.disk}GB | "
                f"Status: {self.status}, Worker: {self.worker_id or '-'}")
