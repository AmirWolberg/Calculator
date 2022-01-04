"""
Module containing all different costume made exception types
"""


class FactorialException(Exception):
    """ Raised when factorial is called on a none natural number """
    pass


class NotSupportedException(Exception):
    """ Raised when a not supported feature is being used """
    pass


class ValidationException(Exception):
    """ Exception raised during validation before starting to
     solve the equation """
    pass


class RunTimeException(Exception):
    """ Exception raised during run time (while solving the equation) """
    pass


class ComplexNumberException(Exception):
    """ Exception raised if a calculation results in a complex number """
    pass
