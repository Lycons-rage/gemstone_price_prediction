# what will be my input path? 
# output: transformed data, pipeline pickle file(need to be saved in artifact folder)

# handling missing values
# feature scaling
# handling numerical values
# handling categorical values

# importing required libraries

import os
import sys
# for resolving any path conflict
current = os.path.dirname(os.path.realpath("data_transformation.py"))
parent = os.path.dirname(current)
sys.path.append(current)

from dataclasses import dataclass

import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTranformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTranformationConfig()
    
    def get_data_transformation_obj(x):
        try:
            logging.info("DATA TRANSFORMATION INITIATED")
            
            # numerical and categorical seggregation
            numerical_features = ['carat', 'depth', 'table', 'x', 'y', 'z']
            categorical_features = ['cut', 'color', 'clarity']
            
            # define custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
            clarity_categories = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            
            logging.info("PIPELINE INITIATED")
            
            # numerical pipeline : first, we will try to handle missing values using SimpleImputer
            # then we will be using StandardScaler for feature scaling
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy = 'median')),
                    # instance_variable      library to be used
                    ('scaler', StandardScaler())
                ]
            )
            
            # categorical pipeline : we just need to perform rank ordinal encoding using OrdinalEncoder
            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                                        # not mode because there's no strategy named mode in SimpleImputer
                    ('encoder', OrdinalEncoder(categories=[cut_categories, color_categories, clarity_categories])),
                                        # categories should be in the same order as features present in the dataset
                    ('scaler', StandardScaler())
                ]
            )
            
            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_features),
                #   variable       pipeline    on which features to apply
                ('cat_pipeline', cat_pipeline, categorical_features)
            ])
            
            logging.info("PIPELINE COMPLETED")        
            return preprocessor
            
        except Exception as e:
            logging.info("ERROR IN TRANFORMATION")
            raise CustomException(e,sys)  
        
    def initiate_data_transformation(self, train_path, test_path):
        # where do we get this train and test path? from the artifacts folder
        try:
            # reading the train and test paths
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            
            logging.info("DATA READ SUCCESSFULLY")
            logging.info(f"Train Data Head : \n{train_df.head().to_string()}")
            logging.info(f"Test Data Head : \n{test_df.head().to_string()}")
            
            logging.info("OBTAINING PREPROCESSOR OBJECT")
            
            preprocessor_obj = self.get_data_transformation_obj()
            
            # defining target columns and dropping the unneccessary features
            target_column_name = 'price'
            drop_columns = [target_column_name, 'id']
            
            # seggregating input feature and target feature
            input_feature_train_df = train_df.drop(columns=drop_columns, axis=1)
            target_feature_train_df = train_df[target_column_name]
            
            input_feature_test_df = test_df.drop(columns=drop_columns, axis=1)
            target_feature_test_df = test_df[target_column_name]
            
            logging.info("APPLYING PREPROCESSOR OBJECT ON TRAINING AND TESTING DATASET")
            
            # fit_transform on train data and transform on test data
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)
            
            logging.info("PREPROCESSOR OBJECT SUCCESSFULLY APPLIED")
            
            # converting the entire data into numpy arrays to be able to lead the arrays quickly
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            
            # now how to save the pickle file, thats where utils.py file come in handy
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_file_path,
                obj = preprocessor_obj
            )
            logging.info("PICKLE FILE CREATED")
            
            return (
                train_arr, 
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            logging.info("EXCEPTION OCCURRED WHILE INITIATING DATA TRANSFORMATION")
            raise CustomException(e, sys)
        
        