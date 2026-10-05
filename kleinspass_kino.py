# SET DEFAULT GIFT SEATS
G_GIFTED_SEAT_COUNT = 5 # temporarily set to 5
# SET SEAT DIMENSIONS
G_SEAT_ROWS = 4
G_SEAT_COLS = 6

import sys # For command line argument sys.argv
from random import randint # For random gift seat assignment
from abc import ABC, abstractmethod # OOP specs

class Customer:
    """Simple Customer object for Seat occupant"""
    id_counter:int = 0
    def __init__(self, prompt:str):
        self.name:str = input(prompt)
        self.id:str = str(Customer.id_counter) 
        Customer.id_counter += 1

class Gift:
    """Interface for Gift implementations"""
    @abstractmethod
    def __str__(self)->str: pass

class Seat(ABC):
    """Interface for Seat implementations"""
    @abstractmethod # return booked status
    def is_booked(self)->bool: pass
    @abstractmethod # action book a seat
    def book_seat(self)->None: pass
    @abstractmethod # return if Seat has a Gift
    def has_gift(self)->bool: pass
    @abstractmethod # set the Seat's Gift
    def set_gift(self, gift:Gift)->None: pass
    @abstractmethod # return the Seat's Gift
    def take_gift(self)->Gift: pass
    @abstractmethod # reset Seat
    def clear_seat(self)->None: pass

class SeatManager(ABC):
    """Interface for SeatManagers needed by Kino clasess"""
    @abstractmethod # return seat objects from seat array
    def get_seat(self, id:str)->Seat: pass
    @abstractmethod # display booked unbooked for customers
    def customer_show_seats(self)->None: pass
    @abstractmethod # display verbose seat data for admins
    def admin_show_seats(self)->None: pass

# SET WHAT THE GIFT IS
class PopcornGift(Gift):
    def __str__(self):
        return "FREE POPCORN 🍿"
    
class BeerGift(Gift):
    def __str__(self):
        return "FREE BEER 🍺"

class KinoSeat(Seat):
    """A KinoSeat that itself stores the entirety of data relevant to a Seat""" 
    def __init__(self):
        self.__customer:Customer = None
        self.__gift = None

    def is_booked(self): return True if self.__customer is not None else False

    def book_seat(self, customer:Customer): 
        """Book a seat, raise an error if seat already booked"""
        if self.is_booked(): raise Exception("!!! Seat already booked.")
        self.__customer = customer

    def has_gift(self): return True if self.__gift else None

    def set_gift(self, gift:Gift):
        """Set the Gift, raise an error if not a Gift instance"""
        if not isinstance(gift, Gift): raise Exception("!!! Not a Gift object.")
        self.__gift = gift
        
    def take_gift(self):
        """Return whatever is in this KinoSeat's gift and dis-own the gift object"""
        if not self.has_gift(): return None
        temp = self.__gift # Note python variables store the Gift object as mutable references
        self.__gift = None # KinoSeat object intentionally loses the reference to the Gift Object
        return temp # Gift reference stored in temp is returned, Gift ownership passed outside

    def clear_seat(self):
        """Reset KinoSeat"""
        self.__customer = None
        self.__gift = None

class Kino2DSeatManager(SeatManager):
    """Manage Seats for Kino classes with 2D lists for storage"""
    def __init__(self, rows_:int, cols_:int):
        self.__rows:int = rows_
        self.__cols:int = cols_ 
        self.__seat_count:int = self.__rows * self.__cols
        self.__seat_list:list = [[KinoSeat() for _ in range(self.__cols)] for _ in range(self.__rows)]
    
    def __map_seat(key:str):
        alphabet = ""
        numeric = "0"
        for k in key:
            if k.isalpha(): alphabet += k.upper()
            elif k.isdigit(): numeric += k
        
        row = 0
        # A is 0, Z is 25, AA is 26 ...
        # A < Z < AA < AZ < BA < BZ ...
        for a in alphabet:
            row = (row*26) + (ord(a) - ord("A") + 1)
        row -= 1 # make it 0 indexed
        col = int(numeric) - 1
        return row, col

    def __seat_coord_to_string_id(self, row:int, col:int):
        num = row + 1 # temporary offset to prevent num -= 1 going out of idx
        alphabet = ""
        # 0 is A, 25 is Z, 26 is AA ...
        # A < Z < AA < AZ < BA < BZ ...
        while num > 0:
            num -= 1 # there is no "0" character, just A to Z 26 characters
            alphabet = chr(num % 26 + ord("A")) + alphabet
            num //= 26
        return alphabet + str(col + 1)
        
    def get_seat(self, id:str):
        """Return the reference to a Seat object, what is returned is mutable so be careful"""
        row, col = self.__map_seat(id)
        if not (0 <= row < self.__rows and 0 <= col < self.__cols):
            raise Exception(f"!!! Seat {id} doesn't exist.")
        return self.__seat_list[row][col]

    def set_random_gifted_seats(self, gifted_seat_count:int):
        """Set the randomized gifted seats"""
        gifted_seat_count = min(gifted_seat_count, self.__seat_count)
        while gifted_seat_count > 0:
            row = randint(0, self.__rows - 1)
            col = randint(0, self.__cols - 1)
            seat:Seat = self.__seat_list[row][col]
            if not seat.has_gift():
                gift = PopcornGift() if (row + col) % 2 == 0 else BeerGift()
                seat.set_gift(gift)
                gifted_seat_count -= 1
    
    def __print_kinoleinwand(self):
        # TODO
        layout = (
            "┌────────────────────────────────────────────────────────┐\n" # !!! Added newline
            "│                      KINOLEINWAND                      │\n" # !!! Added newline
            "└────────────────────────────────────────────────────────┘"
        )
        print(layout)
        
    def customer_show_seats(self):
        # TODO
        """Display seats config for customers, simply booked or unbooked"""
        self.__print_kinoleinwand()
        for row in range(self.__rows):
            print("┌────────┐" * self.__cols)
            #      | booked |
            for col in range(self.__cols):
                seat:Seat = self.__seat_list[row][col]
                txt = "booked" if seat.is_booked() else self.__seat_coord_to_string_id(row, col)
                print(f"│ {txt:<6} │", end="")
            print()
            print("└────────┘" * self.__cols)


    def admin_show_seats(self):
        # TODO
        """Display seats config for admins, verbose"""
        self.__print_kinoleinwand()
        for row in range(self.__rows):
            print("┌────────┐" * self.__cols)
            #      | #AA00$ |
            for col in range(self.__cols):
                seat:Seat = self.__seat_list[row][col]
                txt = "## " if seat.is_booked() else ""
                txt += self.__seat_coord_to_string_id(row, col)
                txt += " $$" if seat.has_gift() else ""
                print(f"│ {txt:<6} │", end="")
            print()
            print("└────────┘" * self.__cols)
    


class Kino:
    def __init__(self, seat_rows:int, seat_cols:int):
        self.seat_manager = Kino2DSeatManager(seat_rows, seat_cols)

    def start(self, gifted_seat_count:int):
        self.seat_manager.set_random_gifted_seats(gifted_seat_count)
        self.seat_manager.customer_show_seats()
        self.seat_manager.admin_show_seats()



if __name__ == "__main__":
    kino = Kino(G_SEAT_ROWS, G_SEAT_COLS)
    # COMMAND LINE ARGUMENTS ex: "... kleinspass_kino.py <int>"
    # whatever is in ... this program only gets the arguments :
    # "kleinspass_kino.py" at idx 0 of sys.argv list
    # <int> at idx 1 of sys.argv list
    # try get and convert argument string at sys.argv[1] to integer
    try: G_GIFTED_SEAT_COUNT = int(sys.argv[1])
    # ignore IndexError when sys.argv[1] doesn't exist ex: "... kleinspass_kino.py"
    # ignore ValueError when sys.argv[1] is not convertible to int
    except Exception: pass

    # majority of program runtime is in the start method ... 
    kino.start(G_GIFTED_SEAT_COUNT)