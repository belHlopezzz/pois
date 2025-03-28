import time


class Process:
    def __init__(self, pid: int, priority: int, memory: int):
        assert pid >= 0, f"PID {pid} must be greater or equal to 0"
        assert -20 <= priority <= 19, f"Priority {priority} must be between -20 and 19"
        assert memory >= 0, f"Memory must be greater or equal to 0"

        self.__pid, self.__priority, self.__state, self.__memory = (
            pid,
            priority,
            "waiting",
            memory,
        )
        self.__start_time, self.__end_time = None, None

    @property
    def pid(self):
        return self.__pid

    @property
    def priority(self):
        return self.__priority

    @property
    def state(self):
        return self.__state

    @property
    def memory(self):
        return self.__memory

    def start(self):
        if self.__start_time is None:
            self.__start_time = time.time()
            self.__state = "running"
        else:
            raise RuntimeError("The process is already running")

    def stop(self):
        if self.__start_time is not None:
            self.__end_time = time.time()
            self.__state = "stopped"
        else:
            raise RuntimeError("The process wasn't launched")

    @property
    def execution_time(self):
        if self.__start_time is None:
            return f"--------"
        if self.__end_time is None:
            end_time = time.time()
        else:
            end_time = self.__end_time

        elapsed_time = end_time - self.__start_time
        hours, rem = divmod(int(elapsed_time), 3600)
        minutes, seconds = divmod(rem, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def __str__(self):
        return f"{self.pid:<10}{self.priority:<10}{self.state:<10}{self.execution_time:<10}{str(self.memory) + "KB":<10}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.pid}, {self.priority}, {self.memory})"
