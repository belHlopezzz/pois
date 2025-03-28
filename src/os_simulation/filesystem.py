from abc import ABC, abstractmethod


class File:
    def __init__(self, name: str, content: str = ""):
        self.name = name
        self.content = content
        self.memory = len(content)

    def __repr__(self):
        return f"File({self.name}, {self.content})"


class Directory:
    def __init__(self, name: str, parent: "Directory" = None):
        self.name = name
        self.parent = parent
        self.subdirectories = {}  # {name of dir: dir}
        self.files = {}  # {name of file: file}

    def add_file(self, file: File):
        if file.name not in self.files:
            self.files[file.name] = file
        else:
            print(f"File {file.name} already exists")

    def add_directory(self, directory: "Directory"):
        if directory.name not in self.subdirectories:
            self.subdirectories[directory.name] = directory
        else:
            print(f"Directory {directory.name} already exists")


class IFileSystem(ABC):
    @abstractmethod
    def create_file(self, file: File):
        pass

    @abstractmethod
    def create_directory(self, name: str):
        pass

    @abstractmethod
    def change_directory(self, name: str):
        pass

    @abstractmethod
    def list_content(self):
        pass

    @abstractmethod
    def read_file(self, name: str):
        pass

    @abstractmethod
    def delete(self, name: str) -> int:
        pass


class FileSystem(IFileSystem):
    DIRECTORY_SIZE = 1

    def __init__(self):
        self.__root = Directory("__root")
        self.__current_directory = self.__root

    @property
    def root(self):
        return self.__root

    @property
    def current_directory(self):
        return self.__current_directory

    def create_file(self, file: File):
        if file.name not in self.__current_directory.files:
            self.__current_directory.add_file(file)
        else:
            print(f"File with name {file.name} already exists")

    def create_directory(self, name: str):
        if name not in self.__current_directory.subdirectories:
            new_directory = Directory(name, self.__current_directory)
            self.__current_directory.add_directory(new_directory)
        else:
            print(f"Folder {name} already exists")

    def change_directory(self, name: str):
        if name == "..":
            if self.__current_directory.parent is not None:
                self.__current_directory = self.__current_directory.parent
        elif name in self.__current_directory.subdirectories:
            self.__current_directory = self.__current_directory.subdirectories[name]
        else:
            print(f"There is no such directory as {name}")

    def list_content(self):
        for directory in self.__current_directory.subdirectories:
            print(f"DIR: {directory}")
        for file in self.__current_directory.files:
            print(f"FILE: {file}")

    def read_file(self, name: str):
        if name in self.__current_directory.files:
            print(self.__current_directory.files[name].content)
        else:
            print(f"There is no such file as {name}")

    def delete(self, name: str) -> int:
        if (
            name in self.current_directory.files
            or name in self.current_directory.subdirectories
        ):
            if name in self.current_directory.files:
                deleting_size = self.current_directory.files[name].memory
                del self.current_directory.files[name]
                return deleting_size
            if name in self.current_directory.subdirectories:
                deleting_size = FileSystem.DIRECTORY_SIZE
                del self.current_directory.subdirectories[name]
                return deleting_size
        else:
            print(f"There is no such file or directory as {name}")
            return 0
