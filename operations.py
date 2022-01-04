"""
Module containing all supported operators
"""
from exceptions import *
from abc import ABC, abstractmethod
from placements import Placement


'''
How to build and add Operator:

Inherit from base class Operator


Initiate the class with the following variables:

placement:
Placement.LEFT -> operator_value
Placement.RIGHT -> value_operator
Placement.BETWEEN -> value_operator_value
Placement.SIGN-> combines left and between and can also
 be chained like right (can come between 2 numbers,
  before a number and after another operator)

precedence:
must be a integer number for example-
1/2/3/4/5/6....

min_values:
integer representing the minimum number of variables the calculation
function of the operator can preform operations on

max_values:
integer representing the maximum number of variables the calculation
function of the operator can preform operations on


Put the following functions in the class:

Calculate:
function that preforms the operation on given number of variables


Add the Operator to the Operators dictionary with a chosen character as
key and the class as value like so:
"Character": CharacterOperatorClass()
'''


class Operator(ABC):
    """ Template for operator """

    @abstractmethod
    def __init__(self):
        """
        Initiates the operator and sets the placement, precedence,
         min_operators and max_operators
        """

        # Placement enum value
        self.placement = None

        # Integer value representing precedence
        self.precedence = None

        # Define minimum amount of values calculation function gets
        self._min_values = None

        # Define maximum amount of values calculation function gets
        self._max_values = None

    @abstractmethod
    def calculate(self, values):
        """
        Does the calculation according to the operator
        :param values: values to be calculated with operator
        :return: get result of operation
        """
        raise NotImplementedError

    def _check_operator_support(self, num_of_values):
        """
        Throw exception if operation doesn't support number
        of given values
        :param num_of_values: number of values given
        :raises NotSupportedException: If number of given values is not
        supported by the calculator raise an exception
        :return:
        """
        if num_of_values < self._min_values or num_of_values >\
                self._max_values:
            raise NotSupportedException("number of given "
                                        "values not supported by operator")


'''
All operator classes
| | | | |
v v v v v
'''
# Precedence 1


class Sub(Operator):
    """ Subtract operator """

    def __init__(self):
        """
        Set placement, precedence, min_operators and max_operators
        """
        Operator.__init__(self)
        self.placement = Placement.SIGN
        self.precedence = 1

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
           -
           subtracts values from first value
           :param values: values to preform operation on
           :return: subtraction of variables
           """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = values[0]
        for val in values[1:]:
            result -= val

        return result


class Add(Operator):
    """ Add operator """

    def __init__(self):
        """
        Set placement, precedence, min_operators and max_operators
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 1

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        +
        Adds the given values up
        :param values: values to preform operation on
        :return: Sum of all given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = 0
        for val in values:
            result += val

        return result

# Precedence 2


class Mul(Operator):
    """ Multiply operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 2

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        *
        Multiplies all given values
        :param values: values to preform operation on
        :return: multiplication of given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = 1
        for val in values:
            result *= val

        return result


class Div(Operator):
    """ Divide operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 2

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        /
        Divides values by first value
        :param values: values to preform operation on
        :return: division of first value by the other given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = values[0]
        for val in values[1:]:
            result /= val

        return result

# Precedence 3


class Pow(Operator):
    """ Power operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 3

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        ^
        Puts the first value to the power of the other values
        :param values: values to preform operation on
        :return: first value to the power of all other given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = values[0]
        for val in values[1:]:
            result **= val

        return result

# Precedence 4


class Mod(Operator):
    """ Module operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 4

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        %
        Gets the module of the first value by all other given values
        :param values: values to preform operation on
        :return: module of first value by all other given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = values[0]
        for val in values[1:]:
            result %= val

        return result

# Precedence 5


class Avg(Operator):
    """ Average operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 5

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        @
        Gets the average of all given values
        :param values: values to preform operation on
        :return: average of given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        avg = 0
        for val in values:
            avg += val
        avg /= len(values)

        result = avg

        return result


class Min(Operator):
    """ Minimum operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 5

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        &
        Gets the minimum values out of all given values
        :param values: values to preform operation on
        :return: minimum value out of given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        minimum = values[0]
        for val in values[1:]:
            if val < minimum:
                minimum = val

        result = minimum

        return result


class Max(Operator):
    """ Maximum operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.BETWEEN
        self.precedence = 5

        self._min_values = 2
        self._max_values = 2

    def calculate(self, values):
        """
        $
        Gets the maximum values out of all given values
        :param values: values to preform operation on
        :return: maximum value out of given values
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        maximum = values[0]
        for val in values[1:]:
            if val > maximum:
                maximum = val

        result = maximum

        return result

# Precedence 6


class Fac(Operator):
    """ Factorial operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.RIGHT
        self.precedence = 6

        self._min_values = 1
        self._max_values = 1

    def calculate(self, values):
        """
        !
        Gets the factorial of given value
        :param values: values to preform operation on
        :return: factorial of value
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        try:
            int_value = int(values[0])
        except ValueError:
            raise FactorialException("Can only factorial natural numbers")

        # Check if number sent to fac is not a whole number
        if int_value != values[0]:
            raise FactorialException("Can only factorial natural numbers"
                                     " (this number is not whole)")

        # Check if number sent to fac is a negative number
        if int_value < 0:
            raise FactorialException("Can only factorial natural numbers"
                                     " (this number is negative)")

        # Preform operation
        factorial = 1
        for x in range(1, int_value + 1):
            factorial = factorial * x

        result = factorial

        return result


class Neg(Operator):
    """ Negative operator """

    def __init__(self):
        """
        Set placement and precedence
        """
        Operator.__init__(self)
        self.placement = Placement.LEFT
        self.precedence = 6

        self._min_values = 1
        self._max_values = 1

    def calculate(self, values):
        """
        ~
        Subtracts given value from 0
        :param values: values to preform operation on
        :return: given value subtracted from 0
        """

        # Check if operation supports number of given operators
        self._check_operator_support(len(values))

        # Preform operation
        result = -values[0]

        return result


'''
Dictionary containing all possible operators supported by the calculator
{Operator character: Operator class instance}
'''
OPERATORS = {"-": Sub(), "+": Add(), "*": Mul(), "/": Div(),
             "^": Pow(), "%": Mod(), "@": Avg(), "&": Min(),
             "$": Max(), "!": Fac(), "~": Neg()}

'''
Contains all operator's characters supported by the calculator
'''
SUPPORTED_OPERATORS = list(OPERATORS.keys())
