from posixpath import split
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtGui
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
        self.user_function = self.ui.lineEdit.text()
        print(self.user_function)

        added_function_parts = self.user_function.strip().split("+")
        function_parts = []
        for part in added_function_parts:
            for p in part.split("-"):
                function_parts.append(p)


# function to test:
# x^2 + 5

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
