"""
Module containing all of the user interfaces and related data
structures
"""
from tkinter import *
from abc import ABC, abstractmethod

'''
How to build and add user interface:

Inherit from base class UserInterface

Initiate with equation_solver function and call _run function 
in __init__

Create _run function

Add user interface to UI_options dictionary as value and 
as a key enter its name
'''


class UserInterface(ABC):
    """ Template for user interface """

    @abstractmethod
    def __init__(self, equation_solver):
        """
        Initiate pointer to equation solver
        :param equation_solver: function that solves the given equation
        """
        self.get_outcome = equation_solver

    @abstractmethod
    def _run(self):
        """
        run and manage the calculator with the given user interface
        :return:
        """
        raise NotImplementedError


class GraphicsTk(UserInterface):
    """ Class taking care of the graphical user interface using tkinter """

    def __init__(self, equation_solver):
        """
         Initiate the class's parameters
         and calls the _build function
        :param equation_solver: function that solves the given equation
        """
        # Call Base class's __init__
        UserInterface.__init__(self, equation_solver)

        # Defining graphics window
        self.master = Tk()

        # Defining Label widget presenting message to user
        self.state_msg = Label()

        # Build the graphical interface
        self._build()

        # Running the main graphics loop
        self._run()

    def _run(self):
        """
        Run the master window's mainloop
        :return:
        """
        self.master.mainloop()

    def _build(self):
        """
        Builds the graphical interface and its widgets and runs its mainloop
        :return:
        """
        # Setting graphic's window parameters
        self.master.title("Calculator")
        self.master.geometry("450x300")
        self.master.resizable(width=False, height=False)
        self.master.configure(background='powder blue')

        # Add 3d border around the Tk window
        Label(self.master, relief=RIDGE,
              justify='right', bd=30, bg="powder blue").pack(side=TOP,
                                                             expand=YES,
                                                             fill=BOTH)

        # Label widget presenting a msg to Enter Input:
        self.input_msg = Label(self.master,
                               text="Enter equation:", bg='powder blue',
                               fg='black', font=("Courier", 12))
        self.input_msg.pack()
        self.input_msg.place(x=40, y=50)

        # Entry widget to enter the equation into
        self.equation_entry = Entry(self.master, bd=1, width=35)
        self.equation_entry.pack()
        self.equation_entry.place(x=190, y=53)
        self.equation_entry.bind('<KeyPress>', self._enter_pressed)

        # Label widget presenting an instruction how to calculate the equation
        self.instruction = Label(
            self.master, text="Press Enter to calculate", bg='powder blue',
            fg='black', font=("Courier", 9))
        self.instruction.pack()
        self.instruction.place(x=220, y=76)

    def _enter_pressed(self, event):
        """
        Calls the equation solver when enter is pressed
        and presents the result on the window
        :param event: what event occurred ->
        what key was pressed in this case
        """

        # Delete previous state_msg
        self.state_msg.destroy()

        try:
            # If Enter was pressed
            if event.keycode == 13:

                # If the equation was solved correctly
                try:
                    # Get the outcome of the equation
                    outcome = self.get_outcome(self.equation_entry.get())
                    # delete all the text in the entry
                    self.equation_entry.delete(0, "end")
                    # Insert result instead
                    self.equation_entry.insert(0, str(outcome[0]))
                    self.state_msg = Label(
                        self.master, text="        Equation Solved",
                        bg='powder blue', fg='green', font=("Courier", 11),
                        wraplength=300)

                # If equation cannot be solved, display error msg
                except Exception as error_message:
                    self.state_msg = Label(
                        self.master, text="Error: " + str(error_message),
                        bg='powder blue', fg='red', font=("Courier", 11),
                        wraplength=300)

                # Pack state_msg and place it
                finally:
                    self.state_msg.pack()
                    self.state_msg.place(x=75, y=100)

        # If the input caused an exception catch it and display
        # the exception error (Input too long may cause exception)
        except Exception as e:
            self.state_msg = Label(
                self.master, text="Input exception: " + str(e),
                bg='powder blue', fg='red',
                font=("Courier", 11), wraplength=300)
            self.state_msg.pack()
            self.state_msg.place(x=75, y=100)


class Console(UserInterface):
    """ Class taking care of console user interface """

    def __init__(self, equation_solver):
        """
        Sets class variables and starts run function
        :param equation_solver: function that solves the given equation
        """
        # Call Base class's __init__
        UserInterface.__init__(self, equation_solver)

        self._run()

    def _run(self):
        """
        Takes care of running the console user interaction
        :return:
        """
        print("\nCalculator On")
        # If keep_running is "x" or "X" the calculator stops running
        keep_running = "Continue"

        # Keep running while user hasn't exited program
        while keep_running.lower() != "x":
            # Surrounded input statement with try and except
            try:
                equation = input("Enter input:")
            except Exception as e:
                print("Error occurred receiving input: " + str(e) +
                      ", please try again")
                continue

            # If the equation was solved correctly
            try:
                # Get outcome of solve_equation function
                outcome = self.get_outcome(equation)
                print(equation + " = " + str(outcome[0]))
                print("Equation solved")

            # Error occurred display error
            except Exception as error_message:
                print(str(error_message))

            # Surrounded input statement with try and except
            try:
                keep_running = input(
                    "Press Enter to continue / Type X to exit")
            except Exception as e:
                print("Error occurred receiving input: " + str(e))
                break  # Exiting user interface


'''
Dictionary holding all user interfaces available
'''
UI_OPTIONS = {"graphicsTk": GraphicsTk, "console": Console}

'''
List of all available user interface options
'''
UI_SUPPORTED_OPTIONS = list(UI_OPTIONS.keys())


def set_ui():
    """
    Sets up the UI by getting input from the console
     as to what user interface to use for the calculator
    :return: chosen user interface OR x meaning to exit program
    """

    # Chosen user interface
    ui = ""

    # Remains true until user chooses valid interface or exits program
    ui_not_chosen = True

    # Loop until a valid UI or X is chosen by the user
    while ui_not_chosen:
        try:
            ui = input(
                "Enter what user interface you"
                " want to use out of given options"
                + str(UI_SUPPORTED_OPTIONS) + " Or enter X to exit program:")
        except Exception as error:
            # Input crashed -> exit program
            print("input crashed: " + str(error))
            return "x"

        # Exiting program
        if ui.lower() == "x":
            return "x"

        # User interface not supported
        elif ui not in UI_SUPPORTED_OPTIONS:
            print("Unsupported user interface option chosen")

        # User interface chosen -> proceed
        else:
            ui_not_chosen = False

    # Return chosen user interface
    return ui
