""" Calculate the price of an order of magnets according to a bulk
pricing scheme. """

import sys


def get_cost(quantity):
    """ Returns total cost and gives ValueError if negative. """
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    if quantity >= 1000:
        price = 0.67
    elif quantity >= 100:
        price = 0.70
    elif quantity >= 50:
        price = 0.72
    else:
        price = 0.75
    return round(quantity * price, 2)
        


if __name__ == "__main__":
    try:
        magnets = int(sys.argv[1])
    except IndexError:
        sys.exit("this program expects a number of magnets as a command-line"
                 " argument")
    except ValueError:
        sys.exit("could not convert " + sys.argv[1] + " into an integer")
    
    try:
        print(get_cost(magnets))
    except ValueError as e:
        sys.exit(str(e))