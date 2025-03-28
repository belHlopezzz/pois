from abc import ABC, abstractmethod
from loading import simulate_loading
from random import randint
import webbrowser
from collections.abc import Iterable


class INetworkProtocol(ABC):
    @abstractmethod
    def send(self, data):
        pass

    @abstractmethod
    def receive(self):
        pass


class TCP(INetworkProtocol):
    # трехстороннее рукопожатие
    @staticmethod
    def __send_syn() -> bool:
        print("Sending SYN...")
        simulate_loading(9e6)
        is_sent = randint(0, 1)
        if is_sent:
            print("SYN sent successfully!")
            return True
        else:
            print("Failed to send SYN. Connection lost.")
            return False

    @staticmethod
    def __recieve_syn_ack() -> bool:
        print("Waiting for SYN ACK...")
        simulate_loading(9e6)
        is_recieved = randint(0, 1)
        if is_recieved:
            print("SYN ACK received successfully!")
            return True
        else:
            webbrowser.open("https://www.youtube.com/watch?v=6EEW-9NDM5k&t=13s")
            return False

    @staticmethod
    def __send_ack():
        print("Sending ACK...")
        simulate_loading(9e5)

    @staticmethod
    def __send_data(data):
        print(f"Sending {data}...")
        simulate_loading(9e7)

    def send(self, data):
        if TCP.__send_syn():
            if TCP.__recieve_syn_ack():
                TCP.__send_ack()
                TCP.__send_data(data)
                print("Message was successfully delivered!")

    def receive(self):
        print("Waiting for incoming message...")
        simulate_loading(9e6)
        print(f"Received new message: {randint(1, 100)}")


class UDP(INetworkProtocol):
    @staticmethod
    def __send_with_loss(data):
        print(f"Sending {data}...")
        simulate_loading(9e6)
        rand_loss = randint(0, len(data))
        print(f"You've just sent: {data[:rand_loss] + data[rand_loss + 1:]}")

    def send(self, data):
        if isinstance(data, Iterable):
            UDP.__send_with_loss(data)
        else:
            print(f"Sending data must be iterable!")

    def receive(self):
        print("Waiting for incoming message...")
        simulate_loading(9e6)
        print(f"Received new message: {randint(1, 100)}")
