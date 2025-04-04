import pytest
from os_simulation.kernel import Kernel
from os_simulation.processes import Process
from os_simulation.resource_manager import MemoryManager, CPUManager
from unittest.mock import patch


# Фикстура для создания экземпляра Kernel
@pytest.fixture
def kernel():
    return Kernel(total_storage=1000)


# Тест инициализации Kernel
def test_kernel_initialization(kernel):
    """Проверка инициализации Kernel с заданным объемом памяти."""
    assert (
        kernel.memory_manager.storage == 1000
    ), "Ошибка: объем памяти не соответствует"
    assert kernel.cpu_manager.utilization == 0, "Ошибка: загрузка CPU не равна нулю"
    assert kernel.pid_counter == 0, "Ошибка: счетчик PID не равен нулю"
    assert kernel.process_table == {}, "Ошибка: таблица процессов не пуста"


# Тест успешного создания процесса
def test_create_process_success(kernel):
    """Проверка успешного создания процесса."""
    kernel.create_process(priority=1, memory=200)
    assert kernel.pid_counter == 1, "Ошибка: счетчик PID не увеличился"
    assert 0 in kernel.process_table, "Ошибка: процесс не добавлен в таблицу"
    assert (
        kernel.process_table[0].priority == 1
    ), "Ошибка: приоритет процесса не соответствует"
    assert (
        kernel.process_table[0].memory == 200
    ), "Ошибка: память процесса не соответствует"
    assert kernel.memory_manager.storage == 800, "Ошибка: память не была выделена"


# Тест успешного запуска процесса
def test_start_process_success(kernel):
    """Проверка успешного запуска процесса."""
    kernel.create_process(priority=1, memory=200)
    with patch.object(Process, "start") as mock_start:
        kernel.start_process(0)
        mock_start.assert_called_once()


# Тест запуска несуществующего процесса
def test_start_process_not_found(kernel):
    """Проверка запуска несуществующего процесса."""
    with patch("builtins.print") as mock_print:
        kernel.start_process(999)
        mock_print.assert_called_with("There is no proccess with pid 999")


# Тест успешной остановки процесса
def test_stop_process_success(kernel):
    """Проверка успешной остановки процесса."""
    kernel.create_process(priority=1, memory=200)
    with patch.object(Process, "stop") as mock_stop:
        kernel.stop_process(0)
        mock_stop.assert_called_once()


# Тест остановки несуществующего процесса
def test_stop_process_not_found(kernel):
    """Проверка остановки несуществующего процесса."""
    with patch("builtins.print") as mock_print:
        kernel.stop_process(999)
        mock_print.assert_called_with("There is no proccess with pid 999")


# Тест выделения памяти
def test_allocate_memory(kernel):
    """Проверка выделения памяти."""
    kernel.allocate_memory(100)
    assert kernel.memory_manager.storage == 900, "Ошибка: память не была выделена"


# Тест освобождения памяти
def test_free_memory(kernel):
    """Проверка освобождения памяти."""
    kernel.allocate_memory(100)
    kernel.free_memory(50)
    assert kernel.memory_manager.storage == 950, "Ошибка: память не была освобождена"
