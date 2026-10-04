# SET DEFAULT GIFT SEATS
gifted_seat_count = 0

import sys

def parse_gift_count_arg():
    # COMMAND LINE ARGUMENTS ex: "... kleinspass_kino.py <int>"
    # whatever is in ... this program only gets the arguments :
    # "kleinspass_kino.py" at idx 0 of sys.argv list
    # <int> at idx 1 of sys.argv list
    global gifted_seat_count
    # try get and convert argument string at sys.argv[1] to integer
    try: gifted_seat_count = int(sys.argv[1])
    # ignore IndexError when sys.argv[1] doesn't exist ex: "... kleinspass_kino.py"
    # ignore ValueError when sys.argv[1] is not convertible to int
    except Exception: pass
    return gifted_seat_count

if __name__ == "__main__":
    int_arg = parse_gift_count_arg()
    print("accepted int from argv", int_arg)