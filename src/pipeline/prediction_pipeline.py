# we need to create a prediction pipeline for new inputs ass well

import sys
import os 

# for resolving any path conflict
current = os.path.dirname(os.path.realpath("data_transformation.py"))
parent = os.path.dirname(current)
sys.path.append(current)

import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass
    
    def predict(self, features):
        try:
            # we need to import preprocessor model
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            model_path = os.path.join("artifacts", "model.pkl")
            
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)
        
            # data scaling
            data_scale = preprocessor.transform(features)
            
            prediction = model.predict(data_scale)
            return prediction
        
        except Exception as e:
            logging.info("EXCEPTION OCCURRED AT PREDICTION PHASE")
            raise CustomException(e, sys)
        
        
# we have to prepare the features too, in order to call predict function
class CustomData:
    def __init__(self,
                 carat:float,
                 depth:float,
                 table:float,
                 x:float,
                 y:float,
                 z:float,
                 cut:str,
                 color:str,
                 clarity:str):
        self.carat = carat
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z
        self.cut = cut
        self.color = color
        self.clarity = clarity
    
    
    def get_data_as_dataframe(self):
        try:
            # we need to convert the data into dataframe
            custom_data_input_dict = {
                'carat':[self.carat],
                'depth':[self.depth],
                'table':[self.table],
                'x':[self.x],
                'y':[self.y],
                'z':[self.z],
                'cut':[self.cut],
                'color':[self.color],
                'clarity':[self.clarity]
            }
        
            df = pd.DataFrame(custom_data_input_dict)
            logging.info("DATAFRAME PREPARED")
            return df
        
        except Exception as e:
            logging.info("EXCEPTION OCCURRED WHILE PREPARING DATAFRAME")
            raise CustomException(e, sys)