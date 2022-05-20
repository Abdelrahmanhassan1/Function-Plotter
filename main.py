import sys
from matplotlib import figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtGui
import sympy
from manigui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # variables
        self.function_plotter_figure = Figure()
        self.function_plotter_figure_canvas = FigureCanvas(
            self.function_plotter_figure)
        self.ui.verticalLayout.addWidget(self.function_plotter_figure_canvas)

        self.max_range_value = 0
        self.min_range_value = 0
        self.valid_chars = ["x", "1", "2", "3", "4", "5", "6",
                            "7", "8", "9", "0", "*", "/", "-", "^", "+", ".", " "]
        self.operators = ["*", "/", "^"]
        self.x_symbol = sympy.symbols("x")

        # handling max and min value inputs to accept just numbers
        validator = QtGui.QDoubleValidator()
        self.ui.min_value_input.setValidator(validator)
        self.ui.max_value_input.setValidator(validator)
        self.ui.step_value_input.setValidator(validator)

        # handling plot button action
        self.ui.pushButton.clicked.connect(self.get_user_function)
        self.ui.pushButton_2.clicked.connect(self.save_figure_from_gui)

    def get_user_function(self):
        try:
            self.user_function = self.ui.function_input.text().strip()
            self.max_range_value = self.ui.max_value_input.text()
            self.min_range_value = self.ui.min_value_input.text()
            self.step_range_value = self.ui.step_value_input.text()

            # check for input validation
            if self.check_entered_three_input(
                    self.user_function, self.min_range_value, self.max_range_value, self.step_range_value):

                self.min_range_value = float(self.min_range_value)
                self.max_range_value = float(self.max_range_value)
                self.step_range_value = float(self.step_range_value)

                equation_expressions = self.calculate_function_expression(
                    self.user_function)

                if not equation_expressions:
                    return

                range_values = np.arange(
                    self.min_range_value, self.max_range_value+0.000001, self.step_range_value)

                full_equation = 0
                x_axis = []
                y_axis = []

                for expression in equation_expressions:
                    full_equation += expression

                # check if the expression is a single number
                if not(isinstance(full_equation, float)):
                    for i in range_values:
                        new_y = full_equation.subs(self.x_symbol, i)
                        if new_y == sympy.zoo:
                            self.raise_error(
                                f"The value x={i} after substitution cause infinity!!")
                            x_axis = []
                            y_axis = []
                            break
                        x_axis.append(i)
                        y_axis.append(new_y)

                else:
                    x_axis = range_values
                    y_axis = np.repeat(full_equation, len(range_values))

                if(len(x_axis) > 0 or len(y_axis) > 0):
                    figure_axes = self.function_plotter_figure.gca()
                    figure_axes.cla()
                    figure_axes.grid(True)
                    figure_axes.set_facecolor((1, 1, 1))
                    figure_axes.set_title("Equation: " + str(full_equation))
                    figure_axes.set_xlabel("x axis")
                    figure_axes.set_ylabel("y axis")
                    figure_axes.plot(x_axis, y_axis)

                self.function_plotter_figure_canvas.draw()
                self.function_plotter_figure_canvas.flush_events()
        except Exception as e:
            print(e)

    def calculate_function_expression(self, function):
        try:
            added_expressions = []
            new_expression = 1

            index = 0
            while True:
                if index == len(function):
                    added_expressions.append(new_expression)
                    break

                char = function[index]
                if char == "x":
                    new_expression *= self.x_symbol
                # if having a power character
                elif char == "^":
                    index += 1
                    power = np.double(function[index])

                    while(power > 1):
                        if function[index-2] == "x":
                            new_expression *= self.x_symbol
                        elif function[index-2].isdigit():
                            new_expression *= np.double(function[index-2])
                        power -= 1

                elif char == "*":
                    index += 1
                    if(function[index] == "x"):
                        new_expression *= self.x_symbol
                    elif(function[index].isdigit()):
                        new_expression *= np.double(function[index])

                elif char == "/":
                    index += 1
                    if(function[index] == "x"):
                        new_expression /= self.x_symbol
                    elif(function[index].isdigit()):
                        new_expression /= np.double(function[index])

                elif char.isdigit():
                    first_index = index
                    while True:
                        index += 1
                        if index == len(function):
                            break
                        next_char = function[index]
                        if next_char.isdigit() or next_char == ".":
                            continue
                        else:
                            break

                    last_index = index
                    index -= 1
                    if first_index == last_index:
                        new_expression *= np.double(function[first_index])
                    else:
                        new_expression *= np.double(
                            function[first_index:last_index])

                elif char == "+":
                    if index != 0:
                        added_expressions.append(new_expression)
                    new_expression = 1

                elif char == "-":
                    if index != 0:
                        added_expressions.append(new_expression)
                    new_expression = -1

                elif char == ".":
                    self.raise_error(
                        "Floating Numbers must start with Digit. (i.e 0.21)")
                    added_expressions = []
                    new_expression = 1
                    return False

                index += 1
            return added_expressions
        except Exception as e:
            print(e)

    def check_entered_three_input(self, function, min, max, step):
        try:
            if function == "" or min == "" or max == "" or step == "":
                self.raise_error(
                    "Function, min, max and step value must be entered.")
                return False

            if (float(step) + float(min)) >= float(max):
                self.raise_error(
                    "Invalid step First value is out of the range")
                return False

            if float(max) <= float(min):
                self.raise_error(
                    "Maximum value must be greater than Minimum value.")
                return False

            for char in function:
                if char not in self.valid_chars:
                    self.raise_error(f"Char ({char}) is not valid!")
                    return False

            first_char = function[0]
            last_char = function[-1]
            if first_char in self.operators or last_char in self.operators:
                self.raise_error(f"The Function Can't Start with operator.")
                return False

            return True
        except Exception as e:
            print(e)

    def raise_error(self, error_message):
        QtWidgets.QMessageBox.about(
            self, "Error", error_message)

    def save_figure_from_gui(self):
        figname, ok = QtWidgets.QInputDialog.getText(
            self, 'input dialog', 'Name of Figure:')
        if ok:
            try:
                self.function_plotter_figure.savefig(
                    f"plot_figures/{figname}.png")
            except Exception as e:
                self.raise_error("Error Figure Not Saved")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
