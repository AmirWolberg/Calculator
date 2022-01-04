"""
Main module of the program ,
run this module to start the up the calculator
"""
from validation import check_validity, check_character_validity_str
from calculations import solve
from conversion import convert_to_list
from user_interface import set_ui, UI_OPTIONS
from exceptions import *


def handle_equation(str_equation):
    """
    Calls all validation, conversion and calculation functions
    on a given string representing an equation
    :param str_equation: string form of the equation given by the user
    :raises RunTimeException: If equation was too long and exceeded
    recursion limit
    :return: the result of the equation or
    throw an appropriate exception
    """

    # Check Character validity of the given string
    check_character_validity_str(str_equation)

    # Convert equation to a list for the solving process
    lst_equation = convert_to_list(str_equation)

    # Check pre calculation validity of the equation
    check_validity(lst_equation)

    # Solve equation, if exception occurs throw it
    try:
        # Solve equation
        return solve(lst_equation)

    # Exceeded maximum recursion depth
    except RecursionError:
        raise RunTimeException("Equation too long,"
                               " Maximum recursion depth exceeded")


if __name__ == "__main__":
    """
    Initiate calculator and user interface 
    """

    # Gets user interface
    UI = set_ui()

    # If valid interface was chosen
    if UI != 'x':

        try:
            # Initiating user interface
            UI_OPTIONS[UI](handle_equation)

        except Exception as e:
            # User interface crashed informing user and exiting program
            print("User interface crashed: " + str(e))

    print("Exiting program...")
