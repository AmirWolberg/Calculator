"""
Module containing placements Enum Declaration
"""
from enum import Enum

'''
Placement option describes the placement of the values
 and number of the values the operator can operate on

How to add placement option:

Add property to Placement Enum in placement.py module
, value of property describes how many 
values the specific placement can receive

Create _cal function for that placement in calculations.py module
that takes care of an operator with the given placement
the _cal function does its calculation by calling the basic _calc
function with the correct values
its can also be responsible for validating given placement, however 
validation function can be added to validations instead of or in addition
to the validation in the newly created _cal function

Add to PlacementCalculations dictionary in calculations module 
Placement.property as key and the _cal function as value like so:
Placement.property: _cal_property

'''


class Placement(Enum):
    """ Enum of possible operator placements """

    # Operator_Value
    LEFT = "1 values left"
    # Value_Operator
    RIGHT = "1 values right"
    # Value_Operator_Value
    BETWEEN = "2 values between"
    # Can be chained or be alone before value Or come between 2 values
    SIGN = "2 values sign"
