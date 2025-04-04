import pytest
import time

from os_simulation.processes import Process


def test_process_creation():
    p = Process(pid=1, priority=0, memory=1024)
    assert p.pid == 1
    assert p.priority == 0
    assert p.memory == 1024
    assert p.state == "waiting"
    assert p.execution_time == "--------"


def test_invalid_pid():
    with pytest.raises(AssertionError, match="PID -1 must be greater or equal to 0"):
        Process(pid=-1, priority=0, memory=1024)


def test_invalid_priority():
    with pytest.raises(AssertionError, match="Priority -21 must be between -20 and 19"):
        Process(pid=1, priority=-21, memory=512)
    with pytest.raises(AssertionError, match="Priority 20 must be between -20 and 19"):
        Process(pid=1, priority=20, memory=512)


def test_invalid_memory():
    with pytest.raises(AssertionError, match="Memory must be greater or equal to 0"):
        Process(pid=1, priority=0, memory=-100)


def test_start_and_state_change():
    p = Process(pid=2, priority=5, memory=512)
    p.start()
    assert p.state == "running"
    assert p.execution_time != "--------"


def test_start_twice_raises():
    p = Process(pid=3, priority=10, memory=2048)
    p.start()
    with pytest.raises(RuntimeError, match="The process is already running"):
        p.start()


def test_stop_without_start_raises():
    p = Process(pid=4, priority=7, memory=512)
    with pytest.raises(RuntimeError, match="The process wasn't launched"):
        p.stop()


def test_stop_changes_state_and_execution_time_format():
    p = Process(pid=5, priority=3, memory=256)
    p.start()
    time.sleep(1)
    p.stop()
    assert p.state == "stopped"
    exec_time = p.execution_time
    assert isinstance(exec_time, str)
    assert len(exec_time.split(":")) == 3


def test_str_representation():
    p = Process(pid=6, priority=1, memory=128)
    expected_start = f"{p.pid:<10}{p.priority:<10}{p.state:<10}"
    assert str(p).startswith(expected_start)


def test_repr_representation():
    p = Process(pid=7, priority=-5, memory=64)
    assert repr(p) == "Process(7, -5, 64)"
