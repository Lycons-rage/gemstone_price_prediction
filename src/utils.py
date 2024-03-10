# all the common functionalities throughout the project to be created here and import as required

# importing required libraries
import os
import sys
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from src.exception import CustomException
from src.logger import logging


# function to save an object into a pickle file
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
            
    except Exception as e:
        logging.info("EXCEPTION OCCURRED IN UTLIS.PY")
        raise CustomException(e, sys)
    
    
def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            
            # train model
            model.fit(X_train, y_train)

            # predict training data
            y_train_pred = model.predict(X_train)            
            # predict test data
            y_test_pred = model.predict(X_test)
            
            # get r2 squared score for training prediction and test prediction
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score
        
        return report
    
    except Exception as e:
        logging.info("EXCEPTION OCCURRED WHILE TRAINING MODEL AND EVALUATION OF MODEL")
        raise CustomException(e, sys)