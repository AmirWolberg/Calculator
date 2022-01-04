"""
Module containing all validation related functions
"""
from operations import OPERATORS, SUPPORTED_OPERATORS
from placements import Placement
from parenthesis import SUPPORTED_CLOSING_PARENTHESIS, \
    SUPPORTED_OPENING_PARENTHESIS
from supported_characters import SUPPORTED_CHARACTERS
from exceptions import *


# Integer representing the maximum equation length allowed
MAXIMUM_EQUATION_LENGTH = 100000


def check_validity(equation):
    """
    Check the validity of an equation -> only validates things
    that can be validated before starting to solve
    The equation is a list representing an equation with its numbers
     as floats and everything else as strings
    :param equation: the equation to validate in list form
    :raises ValidationException: If error in the equation
     was caught during validation
    :return: True if its a valid equation and an error msg otherwise
    """

    # Check if all equation characters are valid
    _check_character_validity_lst(equation)

    # Check validity
    for equation_index in range(0, len(equation)):

        # Validate a certain parenthesis expression in the equation
        if equation[equation_index] in SUPPORTED_OPENING_PARENTHESIS:

            # Index of opening parenthesis
            open_index = equation_index

            # Index of Closing parenthesis
            close_index = equation_index + 1

            # Add 1 to counter when finding opening parenthesis
            # and sub 1 when finding closing parenthesis
            parenthesis_counter = 1

            # Find closing parenthesis that go along
            # with the opening parenthesis we found
            while parenthesis_counter != 0:

                # No closing parenthesis found
                if close_index >= len(equation):
                    raise ValidationException("Validation exception,"
                                              " Missing closing parenthesis")

                if equation[close_index] in SUPPORTED_OPENING_PARENTHESIS:
                    parenthesis_counter += 1

                if equation[close_index] in SUPPORTED_CLOSING_PARENTHESIS:
                    parenthesis_counter -= 1

                close_index += 1

            _check_set_of_parenthesis(equation[open_index:close_index])

        # Check we don't have 2 parenthesis expressions
        # in a row with nothing between like so -> )(
        elif equation_index + 1 < len(equation) and\
                equation[equation_index] in SUPPORTED_CLOSING_PARENTHESIS \
                and equation[equation_index + 1] in\
                SUPPORTED_OPENING_PARENTHESIS:
            raise ValidationException("Validation exception,"
                                      " Can't have 2 parenthesis expressions"
                                      " in a row")

        # Validate operators
        elif equation[equation_index] in SUPPORTED_OPERATORS:

            # Check right operator
            if OPERATORS[equation[equation_index]].placement == Placement.LEFT:
                _check_left_operator(equation, equation_index)

            # Check left operator
            elif OPERATORS[equation[equation_index]].placement ==\
                    Placement.RIGHT:
                _check_right_operator(equation, equation_index)

        # Validate numbers
        else:
            # Check there isn't a number followed by opening parenthesis
            if equation_index + 1 < len(equation) and\
                    (isinstance(equation[equation_index], float)
                     and equation[equation_index + 1]
                     in SUPPORTED_OPENING_PARENTHESIS):
                raise ValidationException("Validation exception,"
                                          " Can't have number with parenthesis"
                                          " expression right after it")

            # Check there isn't a number after parenthesis with
            # no operator between them
            if equation_index > 0 and\
                (isinstance(equation[equation_index], float) and
                 equation[equation_index - 1] in
                 SUPPORTED_CLOSING_PARENTHESIS):
                raise ValidationException("Validation exception,"
                                          " Can't have number with parenthesis"
                                          " expression right before it")

    # Check there aren't any opening parenthesis missing
    parenthesis = 0
    for op in equation:
        if op in SUPPORTED_OPENING_PARENTHESIS:
            parenthesis += 1
        if op in SUPPORTED_CLOSING_PARENTHESIS:
            parenthesis -= 1
    if parenthesis != 0:
        raise ValidationException("Validation exception,"
                                  " Missing Opening parenthesis")

    # Passed all validations , the equation is valid
    return True


def _check_character_validity_lst(equation):
    """
    Checks if the characters of the equation are valid
     (operators or operands)
    :param equation: the equation to validate in list form
    :raises ValidationException: If error in the equation
     was caught during validation
    :return: If equation characters are invalid raise exception
    """
    # Check equation is not empty
    if len(equation) == 0:
        raise ValidationException("Validation exception, Empty equation")

    # Check all items are valid as a part of a mathematical equation
    for op in equation:
        if not isinstance(op, float) and not (op in SUPPORTED_OPERATORS)\
                and not (op in SUPPORTED_OPENING_PARENTHESIS)\
                and not (op in SUPPORTED_CLOSING_PARENTHESIS):
            raise ValidationException("Validation exception, "
                                      "Invalid characters")


def _check_set_of_parenthesis(equation):
    """
    Checks the validity of the outer most parenthesis
     of the equation received
    :param equation: gets a part of the equation surrounded by
     parenthesis (a set of parenthesis)
     :raises ValidationException: If error in the equation
     was caught during validation
    :return: raise exception if parenthesis are invalid
    """

    # Check there are no empty parenthesis
    if len(equation) == 2:
        raise ValidationException("Validation exception,"
                                  " equation Contains empty Parenthesis")

    # Check there are no redundant parenthesis
    temp_index = 1

    #  redundant turns False if there is at least 1 item
    #  inside the parenthesis that is not in another parenthesis
    redundant = True

    # Go over equation until the end of it, or until redundant is False
    while temp_index < len(equation) - 1 and redundant:

        # Found more parenthesis inside, skip them and continue the check
        if equation[temp_index] in SUPPORTED_OPENING_PARENTHESIS:

            # counter Goes down by when closing parenthesis are found
            # and goes up by one when opening parenthesis are found
            counter = 1

            temp_index += 1

            # Find closing parenthesis that go along with the opening
            # parenthesis we found and skip to them
            while counter != 0:

                # No closing parenthesis found
                if temp_index >= len(equation):
                    raise ValidationException("Validation exception,"
                                              " Missing closing parenthesis")

                if equation[temp_index] in SUPPORTED_OPENING_PARENTHESIS:
                    counter += 1

                if equation[temp_index] in SUPPORTED_CLOSING_PARENTHESIS:
                    counter -= 1

                temp_index += 1

        # Found item that is not a parenthesis and
        # not inside inner parenthesis
        if equation[temp_index] not in SUPPORTED_OPENING_PARENTHESIS \
                and equation[temp_index] not in SUPPORTED_CLOSING_PARENTHESIS:
            redundant = False

    # Parenthesis is redundant
    if redundant:
        raise ValidationException("Validation exception,"
                                  " equation Contains redundant parenthesis")

    # Check both parenthesis are of the same type
    if SUPPORTED_OPENING_PARENTHESIS.index(equation[0]) != \
            SUPPORTED_CLOSING_PARENTHESIS.index(equation[-1]):
        raise ValidationException("Validation exception,"
                                  " equation Contains a pair of"
                                  " parenthesis not of the same type")

    # Parenthesis are valid


def _check_left_operator(equation, operator_index):
    """
    Checks the validity of left operator
    :param equation: list form of the equation
    :param operator_index: the index of the operator to validate
    :raises ValidationException: If error in the equation
     was caught during validation
    :return: Throws exception if left operator is invalid
    """

    # Cannot have left operator with a value to its left
    if operator_index != 0 and isinstance(equation[operator_index - 1], float):

        raise ValidationException(str(equation[operator_index]) +
                                  " Validation exception, cannot have left"
                                  " operator with a value to the left of it")

    # Cannot have left operator with closing parenthesis before it
    if operator_index > 0 and equation[operator_index - 1]\
            in SUPPORTED_CLOSING_PARENTHESIS:

        raise ValidationException(str(equation[operator_index]) +
                                  " Validation exception,"
                                  " Can't have left operator with parenthesis"
                                  " expression right before it")

    # Cannot have left operator with no value after it
    if operator_index + 1 >= len(equation)\
            or (equation[operator_index + 1] in SUPPORTED_OPERATORS
                and OPERATORS[equation[operator_index + 1]].placement
                != Placement.LEFT and
                OPERATORS[equation[operator_index + 1]].placement
                != Placement.SIGN):

        raise ValidationException(str(equation[operator_index]) +
                                  " Validation exception, cannot have left"
                                  " operator without value after it")

    # left operator passed validation


def _check_right_operator(equation, operator_index):
    """
    Checks the validity of right operator
    :param equation: list form of the equation
    :param operator_index: the index of the operator to validate
    :raises ValidationException: If error in the equation
     was caught during validation
    :return: Throws exception if right operator is invalid
    """

    # Check what comes after the right operator
    if operator_index + 1 < len(equation):

        # Check there is no right operator with a number/ opening
        #  parenthesis after it (without another operator between them)
        if isinstance(equation[operator_index + 1], float)\
                or equation[operator_index + 1] in\
                SUPPORTED_OPENING_PARENTHESIS:
            raise ValidationException(str(equation[operator_index]) +
                                      " Validation exception,"
                                      " Can't have number/parenthesis"
                                      " expression right after right operator")

        # Check operator following right operator
        elif equation[operator_index + 1] in SUPPORTED_OPERATORS:

            # Check there is no left operator after right operator
            if OPERATORS[equation[operator_index + 1]].placement ==\
                    Placement.LEFT:
                raise ValidationException(str(equation[operator_index]) +
                                          str(equation[operator_index + 1]) +
                                          " Validation exception, Can't have"
                                          " left operator after right operator"
                                          )

            # Check RIGHT operator with higher precedence isn't
            # being chained after right operator with lower precedence
            elif OPERATORS[equation[operator_index + 1]].placement ==\
                    Placement.RIGHT and\
                    (OPERATORS[equation[operator_index + 1]].precedence >
                     OPERATORS[equation[operator_index]].precedence):
                raise ValidationException(str(equation[operator_index]) +
                                          str(equation[operator_index + 1]) +
                                          " Validation exception, Cannot chain"
                                          " right operator with higher"
                                          " precedence after right operator"
                                          " with lower precedence")

    # Cannot have right operator without a value to the left of it
    if operator_index == 0:
        raise ValidationException(str(equation[operator_index]) +
                                  " Validation exception,"
                                  " cannot have right operator without"
                                  " value before it")

    # right operator passed validation


def check_character_validity_str(equation):
    """
    Gets a string representing an equation
    Checks if the characters of the equation are valid
     (operators or operands)
    :param equation: string form of the equation to validate
    :raises ValidationException: If error in the equation
     was caught during validation
    :return: If equation characters are invalid throw exception
    """

    # Limit equation character amount to maximum_equation_length
    if len(equation) > MAXIMUM_EQUATION_LENGTH:
        raise ValidationException("Equation too long, exceeded maximum"
                                  " length allowed (must be under "
                                  + str(MAXIMUM_EQUATION_LENGTH) +
                                  " characters in the equation)")

    # Check all string characters are supported
    for char in equation:

        # char is not supported
        if char not in SUPPORTED_CHARACTERS:
            raise ValidationException(
                "Validation exception, Invalid characters")

    # Equation string characters are valid
