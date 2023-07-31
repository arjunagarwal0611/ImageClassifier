import sys
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QPushButton,  QVBoxLayout, QWidget, QFileDialog, QLabel, QErrorMessage
from PyQt5.QtGui import QImage, QPixmap , QFont 
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import os
import tensorflow as tf
import pickle

 
class TensorFlow_():
    def __init__(self ):
            print("Engine Started")
            
    
    def load(self , folder_location):
            try:
                self.new_model = tf.keras.models.load_model(os.path.join(folder_location , 'model.h5'))
                self.y_classes = pickle.load(open(os.path.join(folder_location , 'classes.pickle') , "rb"))
                return 1 
            except Exception as E:
                return 0


    def get_image_prediction(self , img):
        img = cv2.cvtColor(img , cv2.COLOR_RGB2GRAY)
        img = cv2.resize(img , (120 , 120))
        img = np.array(img)
        img = img.reshape( -1, 120 , 120 , 1)
        y= self.new_model.predict(img/255.)
        y = self.new_model.predict(img/255.)
        index = np.argmax(y[0])
        probability = y[0][index]
        predicted_class  = self.y_classes[index]
        
        return predicted_class , probability


TensorFlow_engine = TensorFlow_()

class ImageWidget(QLabel):

    def __init__(self ):
        super().__init__() 
        self.setScaledContents(True)

    def hasHeightForWidth(self) :
         return self.pixmap() is not None
    
    def heightForWidth(self, w):
        if self.pixmap():
            try:
                return int(w * (self.pixmap().height() / self.pixmap().width()))
            except ZeroDivisionError:
                return 0


def resize_image(image_data, max_img_width, max_img_height):
    scale_percent = min(max_img_width / image_data.shape[1], max_img_height / image_data.shape[0])
    width = int(image_data.shape[1] * scale_percent)
    height = int(image_data.shape[0] * scale_percent)
    newSize = (width, height)
    image_resized = cv2.resize(image_data, newSize, None, None, None, cv2.INTER_AREA)
    return image_resized


def pixmap_from_cv_image(cv_image):
    height, width, _ = cv_image.shape
    bytesPerLine = 3 * width
    qImg = QImage(cv_image.data, width, height, bytesPerLine, QImage.Format.Format_RGB888).rgbSwapped()
    return QPixmap(qImg)



class StartWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Classifier")
        self.setGeometry(100 ,100  , 960 , 540)
        self.import_btn = QPushButton('Import Model')
        self.start_btn = QPushButton('Start')
        self.info = QLabel()
        self.info.setStyleSheet("font-weight: bold;")
        self.info.setFont(QFont('Times', 10))
        self.info.setText("Please select the folder of your model files")
        self.import_btn.clicked.connect(self.choose_model_file)
        self.start_btn.clicked.connect(self.switch_window)
        self.Main_app = MainWindow()
        for btn in [self.import_btn, self.start_btn]:
                btn.setFixedHeight(30)
                btn.setFixedWidth(100)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.import_btn , alignment= Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.info,alignment= Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.start_btn , alignment= Qt.AlignmentFlag.AlignCenter)
        self.central_layout = QVBoxLayout()
        self.main_layout.addWidget(self.Main_app)
        self.Main_app.hide()
        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)



    def choose_model_file(self):
        self.source_folder_name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        print(self.source_folder_name)
        if self.source_folder_name is  None:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No Folder selected')
            error_dialog.exec()

        else :
            
            self.a =TensorFlow_engine.load(self.source_folder_name)
            if self.a ==1:
                self.success = QLabel()
                
                self.success.setText("Model Imported Successfully ! Click start to open Image Classifier")
                self.success.setStyleSheet("font-weight: bold;  color: green;")
                
                self.success.setFont(QFont('Times', 10))
                self.main_layout.addWidget(self.success , alignment=Qt.AlignmentFlag.AlignCenter)
            
            else:
                
                error_dialog = QErrorMessage()
                error_dialog.showMessage('Please select a valid model folder')
                error_dialog.exec()
                

            
    def switch_window(self):
        if self.a ==1:
            self.import_btn.hide()
            self.info.hide()
            self.start_btn.hide()
            self.success.hide()
            self.Main_app.show()
        
        else :
            pass
            





class MainWindow(QMainWindow):

    def __init__(self):
            super().__init__()
            self.setWindowTitle("Image Classifier")
            self.setGeometry(100 ,100  , 960 , 540)
            browse = QPushButton('Browse')
            predict_button = QPushButton('Predict')
            browse.clicked.connect(self.choose_image_source)
            predict_button.clicked.connect(self.process_image)
            for btn in [browse, predict_button]:
                btn.setFixedHeight(30)
                btn.setFixedWidth(100)
            main_Layout = QVBoxLayout()
            top_bar_layout = QHBoxLayout()
            image_bar_layout = QHBoxLayout()
            p_bar_layout = QHBoxLayout()
            self.max_img_height = 400
            self.max_img_width = 600
            self.Prediction = QLabel()
            self.Probability = QLabel()
            self.source_file_name = None
            self.source_image_data = None
            top_bar_layout.addWidget(browse)
            top_bar_layout.addWidget(predict_button)
            self.source_image = ImageWidget()
            self.source_image.setMaximumSize(self.max_img_width , self.max_img_height)
            source_image_layout = QVBoxLayout()
            source_image_layout.addWidget(QLabel("Source image:"))
            source_image_layout.addWidget(self.source_image)
            bottom_bar_layout = QHBoxLayout()
            image_bar_layout.addLayout(source_image_layout)
            bottom_bar_layout.addWidget(self.Prediction)
            p_bar_layout.addWidget(self.Probability)
            main_Layout.addLayout(top_bar_layout)
            main_Layout.addLayout(image_bar_layout)
            main_Layout.addItem(bottom_bar_layout)
            main_Layout.addItem(p_bar_layout)
            widget = QWidget()
            widget.setLayout(main_Layout)
            self.setCentralWidget(widget)


    def choose_image_source(self):
            
            self.source_file_name = QFileDialog.getOpenFileName()[0]
            if not self.source_file_name :
                error_dialog = QErrorMessage()
                error_dialog.showMessage('No image selected')
                error_dialog.exec()
            
            else:
                self.source_image_data = cv2.imread(self.source_file_name)
                source_image_resized = resize_image( self.source_image_data , self.max_img_width , self.max_img_height)
                self.source_image.setPixmap(pixmap_from_cv_image(source_image_resized))



    
    def process_image(self):
        if self.source_image_data is None:
            error_dialog = QErrorMessage()
            error_dialog.showMessage('No image selected')
            error_dialog.exec()
        else:
            self.result_image_data , self.probability = TensorFlow_engine.get_image_prediction(self.source_image_data)
            self.Prediction.setText(str(self.result_image_data))
            self.Prediction.setStyleSheet("font-weight: bold;")
            self.Prediction.setFont(QFont('Times', 40))
            self.Prediction.setAlignment((Qt.AlignmentFlag.AlignCenter))
            self.Probability.setText(f"Probability : {str(self.probability)}")
            self.Probability.setStyleSheet("font-weight: bold;")
            self.Probability.setFont(QFont('Times', 10))
            self.Probability.setAlignment((Qt.AlignmentFlag.AlignCenter))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = StartWindow()
    gui.show()
    sys.exit(app.exec())