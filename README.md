# Calculator---Python-3.6-
Advanced very general calculator in python 3.6 13th grade

# Advanced_Calculator_python_3.6
Made by Amir Wolberg

Advanced calculator written in python 3.6 and tested with pytest 6.2.1, graphics made with tkinter 

Imported libraries:
tkinter (graphical library)
pytest 6.2.1 (testing library)
abc (OOP support library)
enum (OOP support library)

How to set up file:

Download the latest commit version of the Calculator-python3.6.rar file and extract the Calculator file from it
Open the cmd in the Calculator file diretory and run the command main.py to run the program
Or run the tests.py to run the tests

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

User manuel:

Run main.py with python 3.6 (Run the command python main.py in the cmd)
Choose user interface (graphicsTk - graphical interface written using the graphic library tkinter/ console - interface through the console window using print and input)
Enter desired equation to solve and press enter to solve 
You will be presented with the answer or an appropriate error message 
press x to exit

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Developer manuel: 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

The project is divided into 11 Modules:

main.py -
main file of the project, handles running the caculator with the chosen user interface 

operations.py -
module containing all operation types and responsible for implementing them into the calculator using a dictionary

parenthesis.py -
module containing all supported parenthesis types

supported_characters.py -
module containing all characters supported by the calculator

placements.py - 
module containing all different placement types as enum

exceptions.py -
module containing all selfmade exceptions

user_interface.py -
module containing all user interface options and responsible for implementing them using a dictionary and setting them up with the set_ui function

validation.py -
module containing all different validation functions validating the equation in verious stages before solving it

calculations.py -
module containing all types of calculations needed for the calculator to solve the equation and responsible for implementing different calculation for diffrent placement type 
operations using a dictionary

conversion.py -
module containing type conversion methods (convesion the equation from string to list type)

tests.py -
module containing all unit tests, run with pytest framework to test the handle_equation function (only tests the calculator and not the user interfaces)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Future development:

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How to add new operators:

At the operators.py module

Build new operator class like so:

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

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How to add new parenthesis types:

At the parenthesis.py module add to the SUPPORTED_PARENTHESIS dictionary a set of opening and closing parenthesis(each represented by a single character)
the opening parenthesis as key and closing as value like so -> "opening parenthesis" : "closing parenthesis"

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
How to add new user interface:

at the user_interface.py module

Build user interface class like so:

Inherit from base class UserInterface

Initiate with equation_solver function and call _run function 
in __init__

Create _run function

Add user interface to UI_options dictionary as value and 
as a key enter its name

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
how to add new placement type:

at the placement.py and calculations.py modules do the following steps:

Add property to Placement Enum in placements.py, value of property describes how many
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
