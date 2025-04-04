import pytest
from os_simulation.resource_manager import MemoryManager, CPUManager


# Тесты для MemoryManager
def test_memory_manager_initialization():
    total_storage = 1000
    manager = MemoryManager(total_storage)
    assert manager.storage == total_storage


def test_memory_manager_allocate_success():
    manager = MemoryManager(1000)
    manager.allocate(200)
    assert manager.storage == 800


def test_memory_manager_allocate_exact():
    manager = MemoryManager(1000)
    manager.allocate(1000)
    assert manager.storage == 0


def test_memory_manager_allocate_insufficient_storage():
    manager = MemoryManager(1000)
    with pytest.raises(MemoryError, match="No more space on a disk!"):
        manager.allocate(1001)


def test_memory_manager_free():
    manager = MemoryManager(1000)
    manager.allocate(200)
    manager.free(100)
    assert manager.storage == 900


def test_memory_manager_free_more_than_allocated():
    manager = MemoryManager(1000)
    manager.allocate(200)
    manager.free(300)
    assert manager.storage == 1100


def test_cpu_manager_initialization():
    manager = CPUManager()
    assert manager.utilization == 0, "Ошибка инициализации: загрузка не равна нулю"


def test_cpu_manager_allocate_success():
    manager = CPUManager()
    manager.allocate(50)
    assert manager.utilization == 50


def test_cpu_manager_allocate_exceed_max():
    manager = CPUManager()
    manager.allocate(50)
    with pytest.raises(RuntimeError, match="CPU can't handle the load"):
        manager.allocate(51)


def test_cpu_manager_free():
    manager = CPUManager()
    manager.allocate(50)
    manager.free(20)
    assert manager.utilization == 30


def test_cpu_manager_free_more_than_allocated():
    manager = CPUManager()
    manager.allocate(50)
    manager.free(60)
    assert manager.utilization == -10


def test_cpu_manager_free_without_allocation():
    manager = CPUManager()
    manager.free(10)
    assert manager.utilization == -10
