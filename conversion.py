""""
Module containing all conversion functions
"""
from operations import SUPPORTED_OPERATORS
from parenthesis import SUPPORTED_CLOSING_PARENTHESIS, \
    SUPPORTED_OPENING_PARENTHESIS


def convert_to_list(equation):
    """
    Converts the string equation received from user to a
    list of strings(operators/parenthesis) and floats(numbers)
    :param equation: the string form of the equation
    :raises ValueError: if invalid value was entered that cannot be
    converted to a float
    :return: A list holding the equation numbers as
     floats and operators as strings
    """

    # Delete all spaces/tabs/newline from the equation
    equation = equation.replace(" ", "").replace("\t", "").replace("\n", "")

    # Holds string form of current number being iterated over
    current_num = ""

    # Holds the list form of the equation
    equation_list = []

    # Index of the string form of the equation
    equation_index = 0

    # Goes over the equation
    while equation_index < len(equation):

        # If the op is a number/. add it to the current_num variable
        if equation[equation_index] not in SUPPORTED_OPERATORS and not \
                (equation[equation_index] in SUPPORTED_OPENING_PARENTHESIS)\
                and not (equation[equation_index]
                         in SUPPORTED_CLOSING_PARENTHESIS):
            current_num = current_num + equation[equation_index]

        # Reached an operator/parenthesis, putting the number in
        # as a float in the list and afterwards putting the operator
        else:
            # If the current number is not empty
            if current_num != "":
                try:
                    equation_list.append(float(current_num))
                except ValueError:
                    raise ValueError("Cannot convert to float"
                                     " -> invalid value entered")

            # Append operator/parenthesis
            equation_list.append(equation[equation_index])

            # Reset current_num
            current_num = ""

        # Increase index and iterate again
        equation_index += 1

    # Enter the last number into the list
    if current_num != "":
        try:
            equation_list.append(float(current_num))
        except ValueError:
            raise ValueError("Cannot convert to float"
                             " -> invalid value entered")

    return equation_list
