from tqdm.auto import tqdm
import logging
from my_logging import setup_logging
import tensorflow as tf
import tensorflow_addons as tfa
import os
import numpy as np
import pickle
import cv2
import datetime

def long_procedure(filename , model_name):

    if model_name == None:
        
        model_name = "{}_model".format(datetime.datetime.utcnow().isoformat().replace(":", "-"))
        print("Randomly Initiating model Name")
        print(f"Model Name is {model_name}")
    
    print(f"{model_name} : Initiation  Successful")
    list1 = os.listdir(filename)
    x_train = []
    y_train = []
    corrupt_data = 0
    print("Creating Dataset. This may take a while [depending upon the size of the dataset].....")

    try:
        for n , a in enumerate(list1):
            current_dir = os.path.join(filename , a)
            for images in os.listdir(current_dir):
                try:
                    image_array = cv2.imread(os.path.join(current_dir , images) , cv2.IMREAD_GRAYSCALE)
                    image_array = cv2.resize(image_array , (120 , 120))
                    x_train.append(image_array)
                    y_train.append(n)

                except Exception as E:
                    corrupt_data = 1
                    
    except Exception as E:
        print(E)
        print("Make sure the there are only folders inside")
        print("And then Please restart the application ")
        return
    

    if corrupt_data ==1:
        print("Warning : Some Corrupted Data found. Few images might not be included in the training  ")
    print(f"{model_name} : Training Data Created...")
    print("Labels are : {}".format(list1))
    no_classes = len(list1)
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    try:
        model_path = f'model_files/{model_name}'
        os.mkdir(model_path)
        print(f"Created Directory model/{model_name} successfully")
    except Exception as E:
        print(f"Model with name '{model_name}' already exist.")
        model_name = "{}_model".format(datetime.datetime.utcnow().isoformat().replace(":", "-"))
        print("Randomly Initiating New model Name ...")
        print(f"New Model Name is {model_name}")
        model_path = f'model_files/{model_name}'
        os.mkdir(model_path)
        print(f"Created Directory model/{model_name} successfully")

    x_train = x_train.reshape(-1 , 120 , 120 , 1)
    x_train = x_train/255.
    
    setup_logging()
    __logger = logging.getLogger('long_procedure')
    __logger.setLevel(logging.DEBUG)
    
    model = tf.keras.Sequential()

    model.add(tf.keras.layers.Conv2D(64 ,(3,3) , input_shape = x_train.shape[1:] , activation = "relu" ))
    #model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D(pool_size = (2,2)))
    #model.add(tf.keras.layers.Dropout(0.20))

    model.add(tf.keras.layers.Conv2D(64 ,(3,3)  , activation = "relu" ))
    #model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPooling2D(pool_size = (2,2)))
    #model.add(tf.keras.layers.Dropout(0.20))


    model.add(tf.keras.layers.Conv2D(32 , (3 , 3) , activation="relu"))
    #model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.MaxPool2D(pool_size=(2,2)))
    #model.add(tf.keras.layers.Dropout(0.20))

    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation = tf.nn.relu))
    #model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(128 , activation = tf.nn.relu))
    
    model.add(tf.keras.layers.Dense(no_classes , activation  = tf.nn.softmax))
    
    model.compile(optimizer = 'adam' , loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'] , run_eagerly = True)
    tqdm_callback = tfa.callbacks.TQDMProgressBar()
    print(f"{model_name} : Training Started ")
    model.fit(x_train, y_train , epochs = int(8 * no_classes)  , callbacks = [tqdm_callback] , verbose=1)
    
    tqdm_obect = tqdm(tqdm_callback, unit_scale=True, dynamic_ncols=True)
    tqdm_obect.set_description("Model Trained !")
    
    model.save(f'{model_path}/model.h5')
    
    pickle_out= open(f'{model_path}/classes.pickle', "wb")
    pickle.dump( list1, pickle_out)
    pickle_out.close

    print("Model Successfully Trained .")
    print("You Can close the application Now")