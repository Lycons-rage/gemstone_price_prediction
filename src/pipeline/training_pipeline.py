import os
import sys

# for resolving any path conflict
current = os.path.dirname(os.path.realpath("data_transformation.py"))
parent = os.path.dirname(current)
sys.path.append(current)

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer

# running data ingestion

if __name__=='__main__':
    obj=DataIngestion()
    train_data_path, test_data_path = obj.initiate_data_ingestion()
    data_tranformation = DataTransformation()
    train_arr, test_arr, _ = data_tranformation.initiate_data_transformation(train_data_path, test_data_path)
    model_trainer = ModelTrainer()
    model_trainer.initiate_model_training(train_arr, test_arr)