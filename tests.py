"""
Module containing all unit test functions
"""
import pytest
from main import handle_equation


''' 
All test on syntax errors
6 tests
'''
syntax_test_data = [("3^*2",
                     "Illegal operation at: ^ cannot have between"
                     " operator without value after it"),
                    ("(4+5)7", "Validation exception,"
                               " Can't have number with parenthesis"
                               " expression right before it"),
                    ("1!1", "! Validation exception, Can't have"
                            " number/parenthesis expression right"
                            " after right operator"),
                    ("((5+5))", "Validation exception, "
                                "equation"
                                " Contains redundant parenthesis"),
                    ("((1+3)+(1+3)", "Validation exception, "
                                     "Missing closing parenthesis"),
                    ("() + 3", "Validation exception,"
                               " equation Contains empty Parenthesis")
                    ]


@pytest.mark.parametrize("equation, expected_error", syntax_test_data)
def test_syntax(equation, expected_error):
    """
    preform syntax error tests
    test syntax errors throw the correct exceptions
    :param equation: equation being tested
    :param expected_error: error expected to be thrown
    :return: test passed or failed
    """
    with pytest.raises(Exception) as error_message:
        handle_equation(equation)

    assert str(error_message.value) == expected_error


'''
All tests on string invalidity
test 1 checks on empty string
test 2 checks on string with random characters
test 3 checks on string with white spaces
'''
str_test_data = [("", "Validation exception, Empty equation"),
                 ("1+2+שלום", "Validation exception, Invalid characters"),
                 ("             ", "Validation exception, Empty equation")]


@pytest.mark.parametrize("equation, expected_error", str_test_data)
def test_str(equation, expected_error):
    """
    preform string error tests
    test string character errors throw the correct exceptions
    :param equation: equation being tested
    :param expected_error: error expected to be thrown
    :return: test passed or failed
    """
    with pytest.raises(Exception) as error_message:
        handle_equation(equation)

    assert str(error_message.value) == expected_error


'''
All tests on simple equations
test 1-10 check every single operator works
tests 11-15 test on floating point numbers, with basic parenthesis
and with multiple "-" and "~" 
'''
simple_test_data = [("1+2", [3.0]), ("1-2", [-1.0]), ("1*2", [2.0]),
                    ("1/2", [0.5]), ("1%2", [1.0]), ("1^2", [1.0]),
                    ("1@2", [1.5]), ("1&2", [1.0]), ("3!", [6.0]),
                    ("~2", [-2.0]), ("2.5%2", [0.5]), ("2.3*4.5", [10.35]),
                    ("(4!-2)", [22.0]), ("4.51--2", [6.51]), ("2-~-1", [1.0])]


@pytest.mark.parametrize("equation, result", simple_test_data)
def test_simple(equation, result):
    """
    preform simple equation tests
    test if equation's result was as expected
    :param equation: equation being tested
    :param result: expected result of equation
    :return: test passed or failed
    """
    assert handle_equation(equation) == result


'''
All complex equation tests (each equation 20 characters or more)
20 tests
'''
complex_test_data = [("(-5^-2+(6-3*2)/9.3) + 5.21@4", [4.565]),
                     ("(5^-2+(10%3*2)/9.3) + (1&4.1)!", [1.25505376344086]),
                     ("---(-8!+9.01%8.34) -- 900000.1$--1000000000",
                      [1000040319.33]),
                     ("~(1+3-2@5&4$9^2%1.45*-34)", [-117.84456375145827]),
                     (" -~(7012*8%4$3&123 - 87 + 123^0.5 + 4!) - (52@ -52)",
                      [-51.90946349359058]),
                     ("921.12 + -901*(5!%12+3.2)/7.4 + -902",
                      [-370.50162162162155]),
                     ("(1+2) ^ ((-1+~2)*-1)! + (3-1)!", [731.0]),
                     ("( (1+(3+(5*7)-9)@4.56) * (2.5) ) / ~ (-5.12)",
                      [8.681640625]),
                     ("0!+-1*2/3^4%5&6$7@~8", [-1.0]),
                     ("(1/3+2/3+3/3+4/3+5/3+6/3+7/3+8/3)%3", [0.0]),
                     ("----(~((0.5*0.12*0.54*0.91)^100)*-1)",
                      [9.091598593272294e-154]),
                     ("((1*-4/8.1-9) @ (2^(2^3) - 5))", [120.75308641975309]),
                     ("18-6^2+5%4$3+2+4+5+6-------9+7&5/3.2%4.2", [-7.4375]),
                     ("14$5%2&4+4+4-7.7+~((5*3$2)!)", [-1307674367999.7]),
                     ("(0.000000001 * 0.1 * 0.1 * 3 * 0.2) &"
                      " (0.0000000000001)", [1e-13]),
                     ("~(123 @ ((145*2/4%6-6/7) @ (3^5 - 9000)))",
                      [2109.839285714286]),
                     ("52 / (93----98---15*2+3!) % 89.12",
                      [0.6676938880328711]),
                     ("--((1+2@3$3$5$3)%4%3%2%1%-0.5%9)", [0.0]),
                     ("(1^2^3^4^5^6)!/(87$69)", [0.011494252873563218]),
                     ("(420%69) + 9/11 + 8200-70 -- 6969", [15105.818181818182]
                      )]


@pytest.mark.parametrize("equation, result", complex_test_data)
def test_complex(equation, result):
    """
    preform complex equation tests
    test if equation's result was as expected
    :param equation: equation being tested
    :param result: expected result of equation
    :return: test passed or failed
    """
    assert handle_equation(equation) == result


'''
All calculation error tests
5 tests
'''
calculation_test_data = [("8/(5-5)",
                          "Illegal operation at: / Cannot divide by 0"),
                         ("(81-90)!", "Illegal operation at: ! Can only"
                                      " factorial natural numbers"
                                      " (this number is negative)"),
                         ("7.123!", "Illegal operation at: ! Can"
                                    " only factorial natural numbers"
                                    " (this number is not whole)"),
                         ("81^901", "Illegal operation at: ^ Value too"
                                    " large/too small"
                                    "/float too long for calculator"),
                         ("~2^2.2+ 1", "result at ^ is an Unsupported result:"
                                       " (3.7172659624125894+2.7007"
                                       "518095995264j) calculator does not "
                                       "support complex numbers")]


@pytest.mark.parametrize("equation, expected_error", calculation_test_data)
def test_calculation(equation, expected_error):
    """
    preform calculation error tests
    test calculation errors throw the correct exceptions
    :param equation: equation being tested
    :param expected_error: error expected to be thrown
    :return: test passed or failed
    """
    with pytest.raises(Exception) as error_message:
        handle_equation(equation)

    assert str(error_message.value) == expected_error


'''
Sign tests -> tests - cases
7 tests for minus 
'''
sign_test_data = [("(--(--(--(--(4+4)))))", [8.0]),
                  ("--(-5)", [-5.0]), ("--(5)", [5.0]), ("(-4)--(---5)",
                                                         [-9.0]),
                  ("1*---5", [-5.0]), ("1+--5", [6.0]), ("---3!", [-6.0])]


@pytest.mark.parametrize("equation, result", sign_test_data)
def test_sign(equation, result):
    """
    preform sign operator tests
    test if equation's result was as expected
    :param equation: equation being tested
    :param result: expected result of equation
    :return: test passed or failed
    """
    assert handle_equation(equation) == result


'''
operator chaining tests 
7 tests
'''
chain_test_data = [("-----6.12", [-6.12]), ("~~~~~7.12", [-7.12]),
                   ("--~-~~-~~-9", [9.0]), ("~~--~(4-5)", [1.0]),
                   ("4*-~-~~6", [-24.0]), ("4!---~3.3", [27.3]),
                   ("---5--5", [0.0])]


@pytest.mark.parametrize("equation, result", chain_test_data)
def test_chain(equation, result):
    """
    preform operator chaining tests
    test if equation's result was as expected
    :param equation: equation being tested
    :param result: expected result of equation
    :return: test passed or failed
    """
    assert handle_equation(equation) == result
