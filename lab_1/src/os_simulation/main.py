from operating_system import OperatingSystem
from filesystem import FileSystem
from networks import TCP, UDP
from drivers import DriverPackage
from security import DefaultSecurity
from ui import CommandLineInterface

if __name__ == "__main__":
    new_file_system = int(input("Do you want a new FileSystem or Load existance:\t"))
    if new_file_system:
        file_system = FileSystem().load_from_json()
    else:
        file_system = FileSystem()

    while True:
        type_of_network_protocol = input("Type of Network Protocol:\t").upper()
        if type_of_network_protocol == "TCP":
            network_protocol = TCP()
            break
        elif type_of_network_protocol == "UDP":
            network_protocol = UDP()
        else:
            print(f"There is no such Network Protocol as {type_of_network_protocol}")
    total_storage = int(input("Total storage:\t"))
    driver_package = DriverPackage()
    security = DefaultSecurity()
    new_os = OperatingSystem(
        file_system, network_protocol, driver_package, total_storage, security
    )
    cli = CommandLineInterface(new_os)
    cli.start()
