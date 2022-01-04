"""
Module containing all characters supported by the calculator
"""
from operations import SUPPORTED_OPERATORS
from parenthesis import SUPPORTED_OPENING_PARENTHESIS, \
    SUPPORTED_CLOSING_PARENTHESIS

'''
Holds all characters supported by the calculator
'''
SUPPORTED_CHARACTERS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".",
                        " ", "\t", "\n"] + SUPPORTED_CLOSING_PARENTHESIS \
                       + SUPPORTED_OPENING_PARENTHESIS + SUPPORTED_OPERATORS
