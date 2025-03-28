from abc import ABC, abstractmethod


class ISecurity(ABC):
    @abstractmethod
    def authenticate(self, username: str, password: str):
        pass


class DefaultSecurity(ISecurity):
    def __init__(self):
        self.user_info = {"password": "stud", "username": "stud"}

    def authenticate(self, username, password):
        return (
            self.user_info["password"] == password
            and self.user_info["username"] == username
        )
