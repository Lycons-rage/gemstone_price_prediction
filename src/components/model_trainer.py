import os
import sys

# for resolving any path conflict
current = os.path.dirname(os.path.realpath("data_transformation.py"))
parent = os.path.dirname(current)
sys.path.append(current)

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object, evaluate_model

from dataclasses import dataclass


# input for this model trainer? 
@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")
    # pickle file

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
        
    def initiate_model_training(self, train_arr, test_arr):
        try:
            logging.info("SPLITTING DEPENDENT AND INDEPENDENT VARIABLES FORM TRAINING AND TEST SET")
            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            # train multiple models, out of them whichever's accuracy is high we will use that
            models = {
                'linear_reg':LinearRegression(),
                'lasso_reg':Lasso(),
                'ridge_reg':Ridge(),
                'elastic_reg':ElasticNet()
            }
            
            model_report:dict = evaluate_model(X_train, y_train, X_test, y_test, models)
            
            print(model_report)
            print(30*"=")
            logging.info(f"Model Report :\n{model_report}")
            
            # to get the best model from model report
            best_model_score = max(sorted(model_report.values()))
            
            # best model name
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            
            best_model = models[best_model_name]
            
            print(f"BEST MODEL FOUND\n{30*"-"}\nMODEL NAME : {best_model_name}\nSCORE : {best_model_score}")
            print(30*"=")
            logging.info(f"BEST MODEL FOUND\nMODEL NAME : {best_model_name}\nSCORE : {best_model_score}")
            
            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )
            
        except Exception as e:
            logging.info("EXCEPTION OCCURRED IN MODEL TRAINING PHASE")
            raise CustomException(e, sys)