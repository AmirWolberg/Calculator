"""
Module containing all calculation related functions
"""
from operations import SUPPORTED_OPERATORS, OPERATORS
from placements import Placement
from parenthesis import SUPPORTED_CLOSING_PARENTHESIS,\
    SUPPORTED_OPENING_PARENTHESIS
from exceptions import *


def solve(equation):
    """
    Solves the equation using recursion
    finds the inner most parenthesis and inside it finds the
    highest precedence operator , solves that operator
    and recursively calls itself again with that operator
    and numbers around it gone and replaced with the result of
    its operation, throws exceptions if errors in the equation are found
    :param equation: list form of equation
    :raises OverflowError: if result is too long throws over
    flowerror
    :raises NotSupportedException: if operation placement
     is not supported
    :return: The result of the equation in a list
    """
    # Finished solving the equation
    if (len(equation) == 1) and isinstance(equation[0], float):

        # Check if result is too large for calculator
        if equation[0] == float("inf") or equation[0] == float("-inf"):
            raise OverflowError("Value too large/too small/float too long"
                                " for calculator")

        # return result as a list with 1 value
        return equation

    # Find highest precedence operator inside the inner most parenthesis
    highest_precedence_index = _find_highest_precedence(equation)

    '''
    Down below the highest precedence operator's move is made and it and
    the values around it being used
    are removed and replaced with the result
    '''

    # If the operator is not in supportedOperators it means
    # we hit an edge case of a single number in parenthesis -> (x),
    # so highest_precedence_index is the index of x the lone value
    if equation[highest_precedence_index] not in SUPPORTED_OPERATORS:

        # Set what to delete
        delete_from = highest_precedence_index - 1  # ( opening parenthesis
        delete_to = highest_precedence_index + 1  # ) closing parenthesis

        # Get what to replace it with
        result = equation[highest_precedence_index]  # x value in parenthesis

    # Found operation calculate expression around it
    else:

        # Check Operator placement is Supported
        if OPERATORS[equation[highest_precedence_index]].placement\
                in SUPPORTED_PLACEMENTS:

            # Call Placement calculation according to placement of operator
            # outcome = [delete_from, delete_to, result]
            outcome = PLACEMENT_CALCULATIONS[OPERATORS[
                equation[highest_precedence_index]].placement](
                equation, highest_precedence_index)

            # Set what to delete
            delete_from = outcome[0]
            delete_to = outcome[1]

            # Get what to replace it with
            result = outcome[2]

        # No supported option for operator placement
        else:
            raise NotSupportedException("Calculator does not support this sort"
                                        " of operation placement")

    # If this was the last equation in these parenthesis,
    # remove the parenthesis
    if (equation[delete_from - 1] in SUPPORTED_OPENING_PARENTHESIS) and \
            (equation[delete_to + 1] in SUPPORTED_CLOSING_PARENTHESIS):
        equation.pop(delete_from - 1)
        delete_from -= 1
        equation.pop(delete_to)
        delete_to -= 1

    '''
    remove what was just solved and replace it with the result
    '''
    # Remove what we just solved
    for x in range(delete_from, delete_to + 1):
        equation.pop(delete_from)

    # Put the result in
    equation.insert(delete_from, result)

    # Recurse again with smaller equation
    return solve(equation)


def _find_highest_precedence(equation):
    """
    finds the inner most parenthesis in equation
     and in them finds the highest precedence operator's index
    :param equation: list form of equation
    :raises NotSupportedException: if precedence is not supported
    :return: the index of the highest precedence operator
    that should be the next move to happen in the equation
    """

    # Find first inner most parenthesis,
    # by default its the start and end of the equation
    index_opening_parenthesis = 0
    index_closing_parenthesis = len(equation)

    # Find first inner most parenthesis
    for equation_index in range(0, len(equation)):

        # Found opening parenthesis searching for their closing pair
        if equation[equation_index] in SUPPORTED_OPENING_PARENTHESIS:

            index_opening_parenthesis = equation_index
            latest_opening_index = equation_index

            while equation[latest_opening_index]\
                    not in SUPPORTED_CLOSING_PARENTHESIS:

                if equation[latest_opening_index]\
                        in SUPPORTED_OPENING_PARENTHESIS:

                    index_opening_parenthesis = latest_opening_index

                latest_opening_index += 1

            index_closing_parenthesis = latest_opening_index
            break

    # Find first operator in parenthesis's precedence
    first_operator_index = index_opening_parenthesis

    # Go over equation until reaching first operator or end of it
    while equation[first_operator_index] not in SUPPORTED_OPERATORS:
        first_operator_index += 1

        # No operators in parenthesis -> (x)
        if first_operator_index >= index_closing_parenthesis:

            # returns index of x (the lone value in the parenthesis)
            return index_closing_parenthesis - 1

    # Find highest precedence operator inside the inner most parenthesis
    # Set highest precedence as first operator's precedence
    highest_precedence = OPERATORS[equation[first_operator_index]].precedence
    highest_precedence_index = first_operator_index

    # Go over the inner parenthesis and search for
    # highest precedence index
    for inner_parenthesis_index in range(index_opening_parenthesis,
                                         index_closing_parenthesis):

        if equation[inner_parenthesis_index] in SUPPORTED_OPERATORS:

            # Check operator precedence is supported (must be int)
            if not isinstance(
                    OPERATORS[equation[
                        inner_parenthesis_index]].precedence, int):
                raise NotSupportedException("Calculator does not"
                                            " support this sort of"
                                            " operation precedence")

            # If precedence is higher than current highest
            # put it as highest
            if OPERATORS[equation[inner_parenthesis_index]].precedence\
                    > highest_precedence:

                highest_precedence =\
                    OPERATORS[equation[inner_parenthesis_index]].precedence
                highest_precedence_index = inner_parenthesis_index

    return highest_precedence_index


def _calc(op, *args):
    """
    Calculates operator with the values sent (preforms operation)
    :param op: operator to preform operation with
    :param args: variables to preform operation on
    :raises ValueError: if value does not fit operation
    :raises ZeroDivisionError: if operation divides by 0
    :raises OverflowError: if result is too large
    :raises FactorialException: if error regarding factorial was raised
    during operation
    :raises NotSupportedException: if a certain feature is not
    supported by the calculator
    :raises RunTimeException: if a different error occurred during
    run time
    :return: the result of the operation or raises an exception
     if needed
    """
    try:
        # Get result of operation
        result = OPERATORS[op].calculate(args)

        # Check if result is a real number
        if isinstance(result, complex):
            raise ComplexNumberException("Unsupported result: "
                                         + str(result) +
                                         " calculator does not"
                                         " support complex numbers")

        # Convert result to float
        result = float(result)

    except ValueError:
        raise ValueError("Illegal operation at: " + str(op) +
                         " Inappropriate value for certain operand")
    except ZeroDivisionError:
        raise ZeroDivisionError("Illegal operation at: " + str(op) +
                                " Cannot divide by 0")
    except OverflowError:
        raise OverflowError("Illegal operation at: " + str(op) +
                            " Value too large/too small"
                            "/float too long for calculator")
    except FactorialException as e:
        raise FactorialException("Illegal operation at: " + str(op) + " "
                                 + str(e))
    except ComplexNumberException as e:
        raise NotSupportedException("result at " + str(op) + " is an "
                                    + str(e))
    except NotSupportedException as e:
        raise NotSupportedException("Not supported exception at: " +
                                    str(op) + " " + str(e))

    # Other exceptions
    except Exception as e:
        raise RunTimeException(
            "Illegal operation at: " + str(op) + " " + str(e))

    return result


def _sign_after_operator(equation, operator_index):
    """
    calculates the chain of sign operators after given
    operator index and value after them
    :param equation: the equation in list form
    :param operator_index: index of operator before the sign operator
    :raises RunTimeException: if there is no value after the
     sign operator
    :return: exception if calculation went wrong or list containing
    result and the index at the end of the sign chain
    """

    # Use temp_index to iterate over chain of signs
    temp_index = operator_index + 1

    # Iterate until you reach a value or end of equation
    while temp_index < len(equation) and equation[temp_index]\
            in SUPPORTED_OPERATORS and \
            OPERATORS[equation[temp_index]].placement == Placement.SIGN:

        temp_index += 1
        if temp_index >= len(equation) or equation[temp_index]\
                not in SUPPORTED_OPERATORS:
            break

    # If there is no value after the chain of signs, throw exception
    if temp_index >= len(equation) or \
            (equation[temp_index] in SUPPORTED_OPERATORS and
             OPERATORS[equation[temp_index]].placement != Placement.SIGN):
        raise RunTimeException("Illegal operation at: " +
                               str(equation[temp_index - 1]) +
                               " no value after sign operator")

    # temp_index now points to the value
    result = equation[temp_index]
    # calculate chain of signs on result
    for x in range(operator_index + 1, temp_index):
        result = _calc(equation[x], 0, result)

    # Return the result and the index the function advanced to
    return [result, temp_index]


'''
PlacementCalculations functions and dictionary below
'''


def _cal_left(equation, operator_index):
    """
    Calculates equation at given index assuming given index
    is the index of left placement operator
    :param equation: list form of equation
    :param operator_index: index of left placement operator
    :raises RunTimeException: if exception in left placement operator
    occurred during run time
    :return: a list containing where to delete from , where to delete to
    and the result of the calculation
    """

    # If there is a chain of left operators go to the latest one
    temp_index = operator_index

    # The precedence of first chained left operator
    operator_precedence = OPERATORS[equation[operator_index]].precedence

    # Find value after chain of operators
    while not isinstance(equation[temp_index], float):
        temp_index += 1

        # No value found after left placement operator throw exception
        if temp_index >= len(equation):
            raise RunTimeException("Illegal operation at: " +
                                   str(equation[temp_index - 1])
                                   + " No value after operator")

    temp_index -= 1

    # Find latest left placement operator
    while OPERATORS[equation[temp_index]].placement != Placement.LEFT:
        temp_index -= 1
    operator_index = temp_index

    # Throw exception if latest left operator in the left operator chain
    # Has lower precedence than the first
    if operator_precedence > OPERATORS[equation[operator_index]].precedence:
        raise RunTimeException(("Incorrect operator placement at: " +
                                str(equation[operator_index]) + " cannot have"
                                " lower precedence left operator chained after"
                                " higher precedence left operator"))

    # If sign operator comes after the left operator its a sign and
    # thus is valid and needs to be calculated before the operator
    if equation[operator_index + 1] in SUPPORTED_OPERATORS and \
            OPERATORS[equation[operator_index + 1]].placement == \
            Placement.SIGN:

        # Gets list containing [result, end_index]
        outcome = _sign_after_operator(equation, operator_index)

        # Get result of operation
        result = outcome[0]

        end_index = outcome[1]

        # Sets where to delete from and to
        delete_from = operator_index + 1
        delete_to = end_index

    # Calculate left operator with value after it
    else:
        # Calculates left operator with value
        # Get result of operation
        result = _calc(equation[operator_index], equation[
            operator_index + 1])

        # Sets where to delete from and to
        delete_from = operator_index
        delete_to = operator_index + 1

    return [delete_from, delete_to, result]


def _cal_right(equation, operator_index):
    """
    Calculates equation at given index assuming given index is the
    index of right placement operator
    :param equation: list form of equation
    :param operator_index: right placement operator index
    :return: a list containing where to delete from , where to delete to
    and the result of the calculation
    """

    # Calculates right operator with value located to its left

    # Gets result of operation
    result = _calc(equation[operator_index],
                   equation[operator_index - 1])

    # Sets where to delete from and to
    delete_from = operator_index - 1
    delete_to = operator_index

    return [delete_from, delete_to, result]


def _cal_sign(equation, operator_index):
    """
    Calculates equation at given index assuming given index is
    the index of sign placement operator
    :param equation: list form of equation
    :param operator_index: sign placement operator index
    :raises RunTimeException: if exception in sign placement operator
    occurred during run time
    :return: a list containing where to delete from , where to delete to
    and the result of the calculation
    """

    # Make a while loop going over all the sign operators till it reaches
    # a value
    temp_index = operator_index
    while temp_index < len(equation) and equation[temp_index] \
            in SUPPORTED_OPERATORS and \
            OPERATORS[equation[temp_index]].placement == Placement.SIGN:

        # Reached the end of the equation without finding a value
        if temp_index + 1 >= len(equation):
            raise RunTimeException("Illegal operation at: "
                                   + str(equation[-1]) +
                                   " no value after sign operator")
        temp_index += 1

    # Check if we have a value after the multiple sign operators
    if not isinstance(equation[temp_index], float):
        raise RunTimeException("Illegal operation at: "
                               + str(equation[temp_index - 1]) +
                               str(equation[temp_index]) +
                               " no value after sign operator")

    # temp_index is now the index of the value
    value = equation[temp_index]

    # Calculate all signs on value
    for x in range(operator_index + 1, temp_index):
        value = _calc(equation[x], 0, value)

    # Sign between 2 operators
    if operator_index - 1 >= 0 and \
            equation[operator_index - 1] \
            not in SUPPORTED_OPENING_PARENTHESIS:
        result = _calc(equation[operator_index],
                       equation[operator_index - 1], value)
        delete_from = operator_index - 1
        delete_to = temp_index

    # Sign at the start of equation or parenthesis
    else:
        # Gets result of the operation
        result = _calc(equation[operator_index], 0, value)

        # Sets where to delete from and to
        delete_from = operator_index
        delete_to = temp_index

    return [delete_from, delete_to, result]


def _cal_between(equation, operator_index):
    """
    Calculates equation at given index assuming given index is the index of
    between placement operator
    :param equation: list form of equation
    :param operator_index: between placement operator index
    :raises RunTimeException: if exception in between placement operator
    occurred during run time
    :return: a list containing where to delete from , where to delete to
    and the result of the calculation
    """

    # Cannot have between operation with no value before it
    if ((operator_index == 0 or equation[operator_index - 1]
         in SUPPORTED_OPENING_PARENTHESIS)) or (
            equation[operator_index - 1] in SUPPORTED_OPERATORS):
        raise RunTimeException("Illegal operation at: "
                               + str(equation[operator_index]) +
                               " cannot have between"
                               " operator without value before it")

    # Cannot have between operation with no value/ Sign operator after it
    if (operator_index + 1 >= len(equation)) or \
            (operator_index + 1 < len(equation) and
             not isinstance(equation[operator_index + 1],
                            float)
             and not (equation[operator_index + 1] in SUPPORTED_OPERATORS and
                      OPERATORS[equation[operator_index + 1]].placement
                      == Placement.SIGN)):

        raise RunTimeException("Illegal operation at: "
                               + str(equation[operator_index]) +
                               " cannot have between"
                               " operator without value after it")

    # Action is a between operator
    # and the next operator is a sign operator
    elif equation[operator_index + 1] in SUPPORTED_OPERATORS and \
            OPERATORS[equation[operator_index + 1]].placement == \
            Placement.SIGN:
        # Gets list containing [result, end_index]
        outcome = _sign_after_operator(equation, operator_index)

        # Gets result of the operation
        result = outcome[0]

        end_index = outcome[1]

        # Sets where to delete from and to
        delete_from = operator_index + 1
        delete_to = end_index

    # Between operator
    else:
        # Calculates between operator with left and right values
        result = _calc(equation[operator_index],
                       equation[operator_index - 1],
                       equation[operator_index + 1])

        # Sets where to delete from and to
        delete_from = operator_index - 1
        delete_to = operator_index + 1

    return [delete_from, delete_to, result]


'''
Dictionary containing all placement positions as keys and the 
calculation functions responsible for calculations of
each placement as values
'''
PLACEMENT_CALCULATIONS = {Placement.LEFT: _cal_left,
                          Placement.RIGHT: _cal_right,
                          Placement.SIGN: _cal_sign,
                          Placement.BETWEEN: _cal_between}

'''
Holds all supported placements (the ones that have a function taking
care of their calculation case)
'''
SUPPORTED_PLACEMENTS = list(PLACEMENT_CALCULATIONS.keys())
