from processes import Process
from resource_manager import MemoryManager, CPUManager


class Kernel:

    def __init__(self, *, total_storage: int):
        self.process_table = {}
        self.memory_manager = MemoryManager(total_storage)
        self.cpu_manager = CPUManager()
        self.__pid_counter = 0

    @property
    def pid_counter(self):
        return self.__pid_counter

    def create_process(self, *, priority: int, memory: int):
        try:
            new_process = Process(self.__pid_counter, priority, memory)
            self.memory_manager.allocate(memory)
            self.process_table[new_process.pid] = new_process
            self.__pid_counter += 1
        except AssertionError as e:
            print(e)
        except MemoryError as e:
            print(e)

    def start_process(self, pid: int):
        try:
            if pid in self.process_table:
                self.process_table[pid].start()
            else:
                print(f"There is no proccess with pid {pid}")
        except RuntimeError as e:
            print(e)

    def stop_process(self, pid: int):
        try:
            if pid in self.process_table:
                self.process_table[pid].stop()
            else:
                print(f"There is no proccess with pid {pid}")
        except RuntimeError as e:
            print(e)

    def list_processes(self):
        print(
            f"{"PID":<10}{"PRIORITY":<10}{"STATE":<10}{"EXECUTION TIME":<10}{"MEMORY":<10}"
        )
        for value in self.process_table.values():
            print(value)

    def allocate_memory(self, memory: int):
        self.memory_manager.allocate(memory)

    def free_memory(self, memory: int):
        self.memory_manager.free(memory)
