from operating_system import OperatingSystem
from filesystem import File, FileSystem
from networks import TCP
from drivers import DriverPackage
from security import DefaultSecurity


class CommandLineInterface:
    def __init__(self, os: OperatingSystem):
        self.os = os
        self.commands = {
            "help": "Показать список доступных команд",
            "exit": "Выключить систему",
            "fork": "Создать новый процесс",
            "ps": "Вывести список процессов",
            "strp": "Запустить процесс по PID",
            "stpp": "Остановить процесс по PID",
            "touch": "Создать файл",
            "mkdir": "Создать директорию",
            "cd": "Сменить текущую директорию",
            "ls": "Вывести содержимое директории",
            "cat": "Вывести содержимое файла",
            "rm": "Удалить файл или директорию",
            "send": "Отправить сообщение по сети",
            "recieve": "Получить сообщение по сети",
            "dmesg": "Вывести список установленных драйверов",
            "drivermarket": "Вывести доступные драйверы",
            "sudo apt-get install": "Установить новый драйвер",
            "cat /etc/os-release": "Вывести информацию об ОС",
        }

    def start(self):
        user_name, password = input("Username:\t"), input("Password:\t")
        if self.os.launch(user_name, password):
            print("CLI started. Type 'exit' to shutdown.")
            while True:
                command = input(">> ")
                if command == "exit":
                    self.os.shutdown()
                    break
                elif command == "help":
                    print("Available commands:")
                    for cmd, desc in self.commands.items():
                        print(f"{cmd} - {desc}")
                elif command == "fork":
                    priority, memory = int(input("Priority:\t")), int(
                        input("Memory:\t")
                    )
                    self.os.create_process(priority, memory)
                elif command == "ps":
                    self.os.list_processes()
                elif command == "strp":
                    pid = int(input("PID:\t"))
                    self.os.start_process(pid)
                elif command == "stpp":
                    pid = int(input("PID:\t"))
                    self.os.stop_process(pid)
                elif command == "touch":
                    name = input("Name:\t")
                    content = input("File content:\t")
                    file = File(name, content)
                    self.os.create_file(file)
                elif command == "mkdir":
                    name = input("Name:\t")
                    self.os.create_directory(name)
                elif command == "cd":
                    path = input("Path:\t")
                    self.os.change_direcotry(path)
                elif command == "ls":
                    self.os.list_content()
                elif command == "cat":
                    name = input("File Name:\t")
                    self.os.read_file(name)
                elif command == "rm":
                    name = input("Directory or File Name:\t")
                    self.os.delete_file_directory(name)
                elif command == "send":
                    message = input("Message:\t")
                    self.os.send_message(message)
                elif command == "recieve":
                    self.os.recieve_message()
                elif command == "dmesg":
                    self.os.print_installed_drivers()
                elif command == "drivermarket":
                    self.os.print_available_drivers()
                elif command == "sudo apt-get install":
                    type = input("Type:\t").lower()
                    name = input("Name:\t").lower()
                    self.os.install_new_driver(type, name)
                elif command == "cat /etc/os-release":
                    print(self.os)
                else:
                    print(f"Command {command} doesn't exist")
        else:
            print("Authentication failed")


# file_system = FileSystem()
# network_protocol = TCP()
# driver_package = DriverPackage()
# security = DefaultSecurity()
# new_os = OperatingSystem(file_system, network_protocol, driver_package, 100, security)
# cli = CommandLineInterface(new_os)
# cli.start()
