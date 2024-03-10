# input should be path (can be local, or a database)
# output should be train and test data seperated so that we can perform train test split

import os   # if not used then we won't be able to properly deploy it on a linux server
import sys
current = os.path.dirname(os.path.realpath("data_ingestion.py"))
parent = os.path.dirname(current)
sys.path.append(current)
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass   # study about it

from src.components.data_transformation import DataTransformation

# initialise data ingestion configuration

@dataclass
class DataIngestionConfig:
    # we just need two variables
    train_data_path:str = os.path.join('artifacts','train.csv')
                                    # all the filenames we going to use will be inside this folder
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    raw_data_path:str = os.path.join('artifacts', 'raw.csv')
    
# we need to send this entire config for data ingestion

class DataIngestion:
    def __init__(self):
        self.ingestionconfig = DataIngestionConfig()
        # an instance of above config class is created as DataIngestion class is initialised
    
    def initiate_data_ingestion(self):
        logging.info('Data Ingestion Phase starts')
        # created a log as data ingestion starts to keep a track of activity
        try:
            # for exception that may occur during data ingestion
            # code that we need to execute
            df = pd.read_csv('notebooks/data/gemstone.csv')  # change this line when reading from anywhere else
                            # we know why '../' is used
            # we will be using all the genric functions to import from mongo or mysql in utils.py file
            logging.info("Dataset read as pandas dataframe")
            os.makedirs(os.path.dirname(self.ingestionconfig.raw_data_path), exist_ok=True)
            #           giving a pathname           source of path          if already there, ignore
            df.to_csv(self.ingestionconfig.raw_data_path, index=False)
            # raw.csv at the given filepath will be created
            logging.info("Train Test Split")
            train_set, test_set = train_test_split(df, test_size=0.30, random_state=42)
            
            train_set.to_csv(self.ingestionconfig.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestionconfig.test_data_path, index=False, header=True)
            # we are saving train.csv and test.csv
            
            logging.info("Data Ingestion Phase Completed")
            return(
                self.ingestionconfig.train_data_path,
                self.ingestionconfig.test_data_path
            )
            
        except Exception as e:
            logging.info("Exception occurred at Data Ingestion Stage")
            raise CustomException(e,sys)
        
        
if __name__=='__main__':
    obj=DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()
    data_tranformation = DataTransformation()
    train_arr, test_arr, _ = data_tranformation.initiate_data_transformation(train_data_path, test_data_path)