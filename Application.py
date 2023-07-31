
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QErrorMessage
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont 
import sys
from Train_your_model import MainWindow
from Clasifier_App import StartWindow



class final_app(QMainWindow):

    def __init__(self):
        super().__init__()


        self.setWindowTitle('Image_classifier')
        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)
        self.train_btn = QPushButton('Train a new model')
        self.classify_btn = QPushButton('Use an existing model')
        self.info = QLabel()
        self.info.setStyleSheet("font-weight: bold;")
        self.info.setFont(QFont('Times', 10))
        self.info.setText("What do you want to do :")
        self.train_btn.clicked.connect(self.train_btn_clicked)
        self.classify_btn.clicked.connect(self.classify_btn_clicked)

        for btn in [self.classify_btn, self.train_btn]:
                btn.setFixedHeight(50)
                btn.setFixedWidth(180)
        

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.info , alignment= Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.train_btn,alignment= Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.classify_btn , alignment= Qt.AlignmentFlag.AlignCenter)


        self.Training_window = MainWindow()
        self.classify_window = StartWindow()

        self.main_layout.addWidget(self.Training_window)
        self.main_layout.addWidget(self.classify_window)

        self.Training_window.hide()
        self.classify_window.hide()

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    

    def train_btn_clicked(self):

        self.info.hide()
        self.train_btn.hide()
        self.classify_btn.hide()
        self.Training_window.show()
    

    def classify_btn_clicked(self):

        self.info.hide()
        self.train_btn.hide()
        self.classify_btn.hide()
        self.classify_window.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    gui = final_app()
    gui.show()
    sys.exit(app.exec())




