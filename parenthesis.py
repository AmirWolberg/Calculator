"""
Module Containing all Supported opening and closing parenthesis types
"""

'''
Holds all supported parenthesis types

Key is opening parenthesis
Value is closing parenthesis

to add another parenthesis type add to a character representing
the opening and closing parenthesis to the dictionary like so:
"Opening parenthesis": "Closing parenthesis"
'''
SUPPORTED_PARENTHESIS = {"(": ")"}

''' Holds all supported opening parenthesis types '''
SUPPORTED_OPENING_PARENTHESIS = list(SUPPORTED_PARENTHESIS.keys())

''' Holds all supported closing parenthesis types '''
SUPPORTED_CLOSING_PARENTHESIS = list(SUPPORTED_PARENTHESIS.values())
