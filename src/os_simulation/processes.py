class Process:
    processes = []

    def __init__(self, pid: int, priority: int, status: str):
        assert pid >= 0, f"PID {pid} must be greater or equal to 0"
        assert -20 <= priority <= 19, f"Priority {priority} must be between -20 and 19"
        assert (
            status.lower() == "running" or status.lower() == "stopped"
        ), f"There is no such status as {status}"

        self.__pid, self.priority, self.status = pid, priority, status

        Process.processes.append(self)

    def start(self):
        pass

    def stop(self):
        pass
