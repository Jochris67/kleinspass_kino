# SET DEFAULT GIFT SEATS
gifted_seat_count = 0

import sys # For command line argument sys.argv
import random # For random gift seat assignment
from abc import ABC, abstractmethod # OOP specs


class Seat(ABC):
    # Interface
    @abstractmethod
    def book_seat(self): pass

class PrintTicketInterface(ABC):
    # Interface 
    @abstractmethod 
    def print_ticket(self):pass
    @abstractmethod
    def use(self):pass

class Ticket(PrintTicketInterface):
    def __init__(self):
        pass

class Kino:
    def __init__(self):
        pass

    def start(self, gifted_seat_count:int):
        pass

if __name__ == "__main__":
    kino = Kino()
    # COMMAND LINE ARGUMENTS ex: "... kleinspass_kino.py <int>"
    # whatever is in ... this program only gets the arguments :
    # "kleinspass_kino.py" at idx 0 of sys.argv list
    # <int> at idx 1 of sys.argv list
    # try get and convert argument string at sys.argv[1] to integer
    try: gifted_seat_count = int(sys.argv[1])
    # ignore IndexError when sys.argv[1] doesn't exist ex: "... kleinspass_kino.py"
    # ignore ValueError when sys.argv[1] is not convertible to int
    except Exception: pass

    # majority of program runtime is in the start method ... 
    kino.start(gifted_seat_count)