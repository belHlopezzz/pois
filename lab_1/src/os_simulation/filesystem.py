from abc import ABC, abstractmethod
import json


class File:
    def __init__(self, name: str, content: str = ""):
        self.name = name
        self.content = content
        self.memory = len(content)

    def to_dict(self):
        return {"name": self.name, "content": self.content}

    @staticmethod
    def from_dict(data: dict) -> "File":
        return File(data["name"], data["content"])

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

    def to_dict(self):
        return {
            "name": self.name,
            "files": [file.to_dict() for file in self.files.values()],
            "subdirectories": [
                subdir.to_dict() for subdir in self.subdirectories.values()
            ],
        }

    @staticmethod
    def from_dict(data: dict, parent: "Directory" = None) -> "Directory":
        directory = Directory(data["name"], parent=parent)
        for file_data in data.get("files", []):
            file = File.from_dict(file_data)
            directory.add_file(file)
        for subdir_data in data.get("subdirectories", []):
            subdir = Directory.from_dict(subdir_data, parent)
            directory.add_directory(subdir)
        return directory


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

    def __init__(self, root=None, current_dir=None):
        if root is None:
            self.__root = Directory("__root")
            self.__current_directory = self.__root
        else:
            self.__root = root
            self.__current_directory = current_dir

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

    def to_dict(self) -> dict:
        return self.__root.to_dict()

    def save_to_json(self, filepath: str = "filesystem.json"):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)
        print(f"FileSystem saved to {filepath}")

    @staticmethod
    def from_dict(data: dict) -> "FileSystem":
        fs = FileSystem()
        # Переопределяем __root и устанавливаем __current_directory равной корню
        fs._FileSystem__root = Directory.from_dict(data)
        fs._FileSystem__current_directory = fs._FileSystem__root
        return fs

    @classmethod
    def load_from_json(cls, filepath: str = "filesystem.json") -> "FileSystem":
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        fs = cls.from_dict(data)
        print(f"FileSystem loaded from {filepath}")
        return fs
