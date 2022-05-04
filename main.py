from posixpath import split
import string
import sys
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

        # handling max and min value inputs to accept just numbers
        validator = QtGui.QDoubleValidator()
        self.ui.lineEdit_2.setValidator(validator)
        self.ui.lineEdit_3.setValidator(validator)

        # handling plot button action
        self.ui.pushButton.clicked.connect(self.get_user_function)

    def get_user_function(self):
        self.user_function = self.ui.lineEdit.text().strip()

        # first check for valid input function
        valid = ["x", "1", "2", "3", "4", "5", "6",
                 "7", "8", "9", "0", "*", "/", "-", "^", "+"]
        flag = True
        for char in self.user_function:
            if char not in valid:
                QtWidgets.QMessageBox.about(
                    self, "Error", f"Char {char} is not valid!")
                flag = False
                break
        if flag:
            x = sympy.symbols("x")
            y_values = self.user_function.subs(x, 2)
            print(y_values)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
