import json
import os
from loading import simulate_loading

os.chdir(r"C:\Education\University\POIS\second_semester\lab_1\lab_1\src\os_simulation")


class DriverPackage:
    def __init__(self):
        with open("alailable_drivers.json", "r") as f:
            self.__available_drivers = json.load(f)
        self.__installed_drivers = {}

    def install_driver(self, type: str, name: str):
        if type in self.__available_drivers["drivers"]:
            for driver in self.__available_drivers["drivers"][type]:
                if driver["name"] == name:
                    simulate_loading(9e7)
                    self.__installed_drivers[type] = list()
                    self.__installed_drivers[type].append(driver)
                    return

        print("There is no such driver type or driver name")

    def print_available_drivers(self):
        for type in self.__available_drivers["drivers"]:
            print(type.upper())
            for driver in self.__available_drivers["drivers"][type]:
                for name, version in driver.items():
                    print("\t", name, ":", version)
                print()

    def print_installed_drivers(self):
        for type in self.__installed_drivers:
            print(type.upper())
            for driver in self.__installed_drivers[type]:
                for name, version in driver.items():
                    print("\t", name, ":", version)
