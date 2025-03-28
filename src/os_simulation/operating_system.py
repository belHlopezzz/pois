from kernel import Kernel
from filesystem import File, IFileSystem, FileSystem
from networks import INetworkProtocol
from drivers import DriverPackage
from security import ISecurity


class OperatingSystem:
    def __init__(
        self,
        file_system: IFileSystem,
        network_protocol: INetworkProtocol,
        drivers: DriverPackage,
        disk_capacity: int,
        security: ISecurity,
    ):
        self.__kernel = Kernel(total_storage=disk_capacity)
        self.__file_system = file_system
        self.__network_protocol = network_protocol
        self.__driver_package = drivers
        self.is_running = False
        self.__security = security

    @property
    def kernel(self):
        return self.__kernel

    def launch(self, username: str, password: str) -> bool:
        if self.__security.authenticate(username, password):
            self.is_running = True
            return True
        else:
            return False

    def shutdown(self):
        self.is_running = False
        print("System shutdown")

    # Kernel methods implementation
    def create_process(self, priority: int, memory: int):
        self.__kernel.create_process(priority=priority, memory=memory)

    def start_process(self, pid: int):
        self.__kernel.start_process(pid)

    def stop_process(self, pid: int):
        self.__kernel.stop_process(pid)

    def list_processes(self):
        self.__kernel.list_processes()

    # File system methods implementation
    def create_file(self, file: File):
        try:
            self.__kernel.allocate_memory(file.memory)
            self.__file_system.create_file(file)
        except MemoryError as e:
            print(e)

    def create_directory(self, name: str):
        try:
            self.__kernel.allocate_memory(FileSystem.DIRECTORY_SIZE)
            self.__file_system.create_directory(name)
        except MemoryError as e:
            print(e)

    def change_direcotry(self, name: str):
        self.__file_system.change_directory(name)

    def list_content(self):
        self.__file_system.list_content()

    def read_file(self, name: str):
        self.__file_system.read_file(name)

    def delete_file_directory(self, name: str):
        self.__kernel.free_memory(self.__file_system.delete(name))

    # Network protocol
    def send_message(self, data):
        self.__network_protocol.send(data)

    def recieve_message(self):
        self.__network_protocol.receive()

    # Drivers methods
    def print_available_drivers(self):
        self.__driver_package.print_available_drivers()

    def print_installed_drivers(self):
        self.__driver_package.print_installed_drivers()

    def install_new_driver(self, type: str, name: str):
        self.__kernel.allocate_memory(len(type) * 3)
        self.__driver_package.install_driver(type, name)

    def __str__(self):
        return f"Operating System: \n\tUser: {self.__security.user_info["username"]}\n\tFileSystem: {self.__file_system.__class__.__name__}\n\tNetwork Protocol: {self.__network_protocol.__class__.__name__}\n\tInstalled Drivers: {self.print_installed_drivers()}\n\tFree storage: {self.__kernel.memory_manager.storage}"
