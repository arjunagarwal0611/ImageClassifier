from MyPyQtGUI import MainApp 
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QLabel, QErrorMessage

from PyQt5.QtCore import Qt
import sys


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Your Model')
        self.terminal = MainApp()
        self.setMinimumWidth(1280)
        self.setMinimumHeight(720)
        browse = QPushButton('Browse Dataset')
        browse.clicked.connect(self.file_info)
        browse.setFixedHeight(40)
        browse.setFixedWidth(120)
        
        
        terminal_layout = QVBoxLayout()
        label1 = QLabel("Select the place where you have images sorted in folders with class names as folder names ")
        label1.setStyleSheet("font-weight: bold;")

        terminal_layout.addWidget( label1, alignment=Qt.AlignmentFlag.AlignCenter)
        terminal_layout.addWidget(self.terminal)
        main_layout = QVBoxLayout()
        main_layout.addWidget(browse , alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        main_layout.addLayout(terminal_layout)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        

    def file_info(self):
        self.source_folder_name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        
        if self.source_folder_name is  None:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No Folder selected')
            error_dialog.exec()

        else :
            
            self.terminal.take_filefolder(self.source_folder_name)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    UIWindow = MainWindow()
    UIWindow.show()
    sys.exit(app.exec_())