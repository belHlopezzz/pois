from abc import ABC, abstractmethod


class IResouceManager(ABC):
    @abstractmethod
    def allocate(self):
        pass

    @abstractmethod
    def free(self):
        pass


class MemoryManager(IResouceManager):
    def __init__(self, total_storage: int):
        self.__storage = total_storage

    @property
    def storage(self):
        return self.__storage

    def allocate(self, memory_amount: int):
        if self.__storage - memory_amount >= 0:
            self.__storage -= memory_amount
        else:
            raise MemoryError("No more space on a disk!")

    def free(self, memory_amount: int):
        self.__storage += memory_amount


class CPUManager(IResouceManager):
    def __init__(self):
        self.__utilization = 0

    @property
    def utilization(self):
        return self.__utilization

    def allocate(self, load: int):
        if self.__utilization + load < 100:
            self.__utilization += load
        else:
            raise RuntimeError("CPU can't handle the load")

    def free(self, load: int):
        self.__utilization -= load
