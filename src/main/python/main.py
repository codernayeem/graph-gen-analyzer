from fbs_runtime.application_context import ApplicationContext

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QPixmap
import matplotlib.pyplot as plt
import numpy as np

from math import *
from dialogs import Ui_AboutPage

appctxt = ApplicationContext()

class MainWindow(QMainWindow):
    app_version = appctxt.build_settings['version']
    app_name = appctxt.build_settings['app_name']
    main_icon = appctxt.get_resource('Icon.ico')

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.app_name)
        self.resize(800, 700)
        font = QFont()
        font.setPointSize(11)
        self.setFont(font)
        self.setup_toolbar()
        self.about_page = None

        # Create central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        #create left widget
        self.left_widget = QWidget(self.central_widget)
        self.left_widget.setObjectName("left_widget")
        self.left_widget.setStyleSheet("#left_widget{background: rgb(230, 231, 255);}")

        #create right widget
        self.right_widget = QWidget(self.central_widget)

        #create input fields and buttons
        self.points_input_type = QComboBox(self.left_widget)
        self.points_input = QTextEdit(self.left_widget)
        self.x_list_input = QTextEdit(self.left_widget)
        self.y_list_input = QTextEdit(self.left_widget)
        self.poly_fit_check = QCheckBox("Fit polinomiyal", self.left_widget)
        self.degree_input = QComboBox(self.left_widget)
        self.generate_graph_button = QPushButton("Generate Graph", self.left_widget)
        self.tan_point_x_input = QLineEdit(self.left_widget)
        self.slope_calculate_bt = QPushButton("Calculate Slope", self.left_widget)
        self.tan_length_input = QLineEdit("1", self.left_widget)
        self.graph_slope_bt = QPushButton("Graph with Slope", self.left_widget)

        self.coeffs_data = QTextEdit(self.right_widget)
        self.equation_input = QTextEdit(self.right_widget)
        self.ideal_value_input = QLineEdit(self.right_widget)
        self.generate_value_button = QPushButton("Calculate Result", self.right_widget)

        #create labels
        self.points_type_label = QLabel("Points Type :", self.left_widget)
        self.x_list_label = QLabel("x Values:", self.left_widget)
        self.y_list_label = QLabel("y Values:", self.left_widget)
        self.points_label = QLabel("Graph Points: (x, y)", self.left_widget)
        self.degree_label = QLabel("Degree", self.left_widget)
        self.tan_point_x_label = QLabel("Tangent point (x):", self.left_widget)
        self.tan_point_x_y_label = QLabel("Tangent point (x, y):", self.left_widget)
        self.tan_length_label = QLabel("Tangent Length:", self.left_widget)
        self.slope_label = QLabel("Slope:", self.left_widget)

        self.coeffs_label = QLabel("Coeffs: ", self.right_widget)
        self.equation_label = QLabel("Equation: ", self.right_widget)
        self.eq_result_label = QLabel("Evaluated Result:", self.right_widget)
        self.ideal_value_label = QLabel("Ideal Value:", self.right_widget)
        self.error_label = QLabel("Error:", self.right_widget)

        #set buddy for labels
        self.points_type_label.setBuddy(self.points_input_type)
        self.points_label.setBuddy(self.points_input)
        self.x_list_label.setBuddy(self.x_list_input)
        self.y_list_label.setBuddy(self.y_list_input)
        self.degree_label.setBuddy(self.degree_input)
        self.tan_point_x_label.setBuddy(self.tan_point_x_input)

        self.coeffs_label.setBuddy(self.coeffs_data)
        self.equation_label.setBuddy(self.equation_input)
        self.ideal_value_label.setBuddy(self.ideal_value_input)

        #create layout for left widget
        left_layout = QGridLayout()
        
        left_layout.addWidget(self.points_type_label, 0, 0)
        left_layout.addWidget(self.points_input_type, 0, 1)
        left_layout.addWidget(self.x_list_label, 1, 0, 1, 2)
        left_layout.addWidget(self.x_list_input, 2, 0, 1, 2)
        left_layout.addWidget(self.y_list_label, 3, 0, 1, 2)
        left_layout.addWidget(self.y_list_input, 4, 0, 1, 2)
        left_layout.addWidget(self.points_label, 5, 0, 1, 2)
        left_layout.addWidget(self.points_input, 6, 0, 1, 2)
        left_layout.addWidget(self.poly_fit_check, 7, 0, 1, 2)
        left_layout.addWidget(self.degree_label, 8, 0)
        left_layout.addWidget(self.degree_input, 8, 1)
        left_layout.addWidget(self.generate_graph_button, 9, 0, 1, 2)

        left_layout.addWidget(self.tan_point_x_label, 10, 0)
        left_layout.addWidget(self.tan_point_x_input, 10, 1)
        left_layout.addWidget(self.tan_point_x_y_label, 11, 0, 1, 2)
        left_layout.addWidget(self.slope_label, 12, 0, 1, 2)
        left_layout.addWidget(self.slope_calculate_bt, 13, 0, 1, 2)
        left_layout.addWidget(self.tan_length_label, 14, 0)
        left_layout.addWidget(self.tan_length_input, 14, 1)
        left_layout.addWidget(self.graph_slope_bt, 15, 0, 1, 2)
        
        self.left_widget.setLayout(left_layout)

        #create layout for right widget
        right_layout = QGridLayout()
        right_layout.addWidget(self.coeffs_label, 0, 0, 1, 2)
        right_layout.addWidget(self.coeffs_data, 1, 0, 1, 2)
        right_layout.addWidget(self.equation_label, 2, 0, 1, 2)
        right_layout.addWidget(self.equation_input, 3, 0, 1, 2)
        right_layout.addWidget(self.eq_result_label, 4, 0, 1, 2)
        right_layout.addWidget(self.ideal_value_label, 5, 0)
        right_layout.addWidget(self.ideal_value_input, 5, 1)
        right_layout.addWidget(self.error_label, 6, 0, 1, 2)
        right_layout.addWidget(self.generate_value_button, 7, 0, 1, 2)
        self.right_widget.setLayout(right_layout)

        #set default values for combo box
        self.points_input_type.addItems(["[x, ...], [y, ...]", "(x, y)"])
        self.degree_input.addItems(["1 - Linear", "2 - Quadratic", "3", "4", "5", "6", "7", "8", "9", "10"])
        self.degree_input.setCurrentIndex(1)

        #connect buttons to functions
        self.points_input_type.currentIndexChanged.connect(self.selectPointsType)
        self.poly_fit_check.setChecked(True)
        self.poly_fit_check.stateChanged.connect(lambda i: self.degree_input.setDisabled(True if not i else False))
        self.generate_graph_button.clicked.connect(self.generate_graph)
        self.slope_calculate_bt.clicked.connect(self.generate_slope)
        self.graph_slope_bt.clicked.connect(lambda : self.generate_graph(with_slope=True))
        self.generate_value_button.clicked.connect(self.generate_value)

        #Placehoder text
        self.equation_input.setPlaceholderText("Here, you can access slope, coeffs, tangent point. Also you can access anything from math library. Like sin, cos, pi etc. Use proper brackets.")
        self.x_list_input.setPlaceholderText("Ex. 1, 2, 3, ...")
        self.y_list_input.setPlaceholderText("Ex. 1, 2, 3, ...")
        self.points_input.setPlaceholderText("EX. (1, 2) (2, 4) ...")

        # initialize things
        self.points_input.setDisabled(True)
        self.coeffs_data.setReadOnly(1)
        self.coeffs_data.setStyleSheet("color: black; border: 2px solid gray;")
        self.statusbar = self.statusBar()
        
        # self.layout.setColumnStretch(0, 0)
        self.layout.addWidget(self.left_widget, 0, 0)
        self.layout.addWidget(self.right_widget, 0, 1)

        self.resetAll()

    def setup_toolbar(self):
        self.toolBar = QToolBar(self)
        self.toolBar.setWindowTitle("Toolbar")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(28, 28))
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.actionAbout_the_Author = QAction(self)
        self.actionAbout_the_Author.setText("About the Author")
        self.actionExit = QAction(self)
        self.actionExit.setText("Exit")
        self.actionReset = QAction(self)
        self.actionReset.setText("Reset")

        self.toolBar.addAction(self.actionReset)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAbout_the_Author)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)

        self.actionExit.triggered.connect(sys.exit)
        self.actionReset.triggered.connect(self.resetAll)
        self.actionAbout_the_Author.triggered.connect(self.see_about)

    def resetAll(self):
        self.status('Ready')

        self.coeffs = None
        self.slope = None
        self.point = None

        self.x_list_input.setPlainText('')
        self.y_list_input.setPlainText('')
        self.points_input.setPlainText('')
        self.equation_input.setPlainText('')
        self.coeffs_data.setPlainText('N/A')
        self.tan_point_x_input.setText('')
        self.tan_length_input.setText('1')
        self.ideal_value_input.setText('')
        self.degree_input.setCurrentIndex(1)
        
        self.tan_point_x_y_label.setText('Tangent point (x, y):')
        self.slope_label.setText('Slope')
        self.eq_result_label.setText('Evaluated result:')
        self.error_label.setText('Error:')
        self.slope_label.setText('Slope')
    
    def see_about(self):
        if self.about_page is None:
            self.about_page = QWidget()
            self.about_page.ui = Ui_AboutPage()
            self.about_page.ui.setupUi(self.about_page)
            self.about_page.ui.version.setText(f'v{self.app_version}')
            self.about_page.ui.icon.setPixmap(QPixmap(self.main_icon))
            self.about_page.ui.name.setText(self.app_name)
        self.about_page.destroy()
        self.about_page.show()

    def status(self, msg, sec=None):
        if sec is None:
            self.statusbar.showMessage(msg)
        else:
            self.statusbar.showMessage(msg, sec)

    def selectPointsType(self, index):
        if(index == 0):
            self.points_input.setDisabled(1)
            self.x_list_input.setDisabled(0)
            self.y_list_input.setDisabled(0)
        else:
            self.x_list_input.setDisabled(1)
            self.y_list_input.setDisabled(1)
            self.points_input.setDisabled(0)

    def get_x_y_list(self):
        if self.points_input_type.currentIndex() == 0:
            x_list = self.x_list_input.toPlainText().strip()
            y_list = self.y_list_input.toPlainText().strip()

            if not (x_list and y_list):
                self.status("Please Enter x list & y list")
                return False, [], []

            x_list = x_list.split(",")
            y_list = y_list.split(",")
            try:
                x = [float(i) for i in x_list]
                y = [float(i) for i in y_list]
            except:
                self.status("x list, y list Parsing Error", 5000)
                return False, [], []
            if (len(x) != len(y)):
                self.status("Length of x_list and y_list is not same.", 5000)
                return False, [], []
        else:
            points = self.points_input.toPlainText().strip()
            if not points:
                self.status("Please Enter (x, y) points")
                return False, [], []
            #parse points into x and y lists
            x = []
            y = []
            try:
                for point in points.split(" "):
                    x.append(float(point.split(",")[0]))
                    y.append(float(point.split(",")[1]))
            except:
                self.status("(x, y) Parsing Error", 5000)
                return False, [], []
        return True, x, y

    def generate_graph(self, with_slope=False):
        ok, x, y = self.get_x_y_list()
        if not ok:
            return

        degree = self.degree_input.currentIndex()+1
        #plot graph
        plt.close()
        plt.clf()

        plt.plot(x, y, 'o', label='Original Points')
        
        if self.poly_fit_check.isChecked():
            self.coeffs = np.round(np.polyfit(x, y, degree), 11)
            self.coeffs_data.setPlainText(str(list(self.coeffs)))
            xs = np.linspace(min(x), max(x), 100)
            ys = np.polyval(self.coeffs, xs)
            plt.plot(xs, ys, 'r-', label="Best Fit Polynomial")

            if with_slope:
                val_x, val_y = self.generate_slope()
                if not (val_x is not None and val_y is not None):
                    return
                try:
                    tan_l = round(float(self.tan_length_input.text()), 10)
                    intercept = val_y - self.slope * val_x

                    x_tan = np.linspace(val_x-tan_l, val_x+tan_l, 10)
                    y_tan = self.slope*x_tan + intercept
                    plt.plot(x_tan, y_tan, 'b-', label='Slope')
                    plt.plot([val_x], [val_y], 'y.', label='Tangent Point')

                except Exception as e:
                    self.status(str(e), 5000)

        plt.legend()
        plt.show()

    def generate_slope(self):
        # if (self.degree_input.currentIndex()+1 == 1) and len(self.coeffs) == 2(:
        #     self.slope = self.coeffs[0]
        #     self.slope_label.setText(f"Slope : {self.slope}"))
        
        if self.coeffs is not None and len(self.coeffs) != 0:
            try:
                tanx = self.tan_point_x_input.text().strip()
                if tanx:
                    tan_x = round(float(self.tan_point_x_input.text()), 10)
                else:
                    self.status("Please input tanget (x), where the slope is needed")
                    return None, None
            except Exception as e:
                self.status(str(e), 5000)
                return None, None
            tan_y = round(np.polyval(self.coeffs, [tan_x])[0], 9)
            self.tan_points = (tan_x, tan_y)
            self.tan_point_x_y_label.setText(f"Tangent Point : ({tan_x}, {tan_y})")

            derivative = np.polyder(self.coeffs)
            self.slope = np.polyval(derivative, tan_x)
            self.slope_label.setText(f"Slope : {self.slope}")

            self.point = (tan_x, tan_y)

            return tan_x, tan_y
        else:
            self.status("Please Generate the graph first")
    
    def generate_value(self):
        equation = self.equation_input.toPlainText().strip()
        ideal_value = self.ideal_value_input.text().strip()

        if not equation:
            self.status("Please Enter an Equation")
            return
        
        #evaluate equation
        coeffs = self.coeffs
        slope = self.slope
        try:
            result = round(float(eval(equation)), 10)
            self.eq_result_label.setText(f"Evaluated Result : {f_str(result)}")
        except SyntaxError as e:
            self.status("Syntax error in Equation", 5000)
            return
        except Exception as e:
            print(e)
            self.status("Error in Equation Evaluation", 5000)
            return

        try:
            if ideal_value:
                ideal_value = float(ideal_value)
                error = round(abs(ideal_value - result) / ideal_value * 100, 10)
                self.error_label.setText(f"Error : {f_str(error)} %")
        except:
            self.status("Invalid Ideal Value")

def f_str(x):
    s = f"{x:.10f}"
    while 1:
        if s[-1] == '0':
            s = s[:-1]
        elif s[-1] == '.':
            s = s[:-1]
            break
        else:
            break
    return s

if __name__ == '__main__':
    window = MainWindow()
    window.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
