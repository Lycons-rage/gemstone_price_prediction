# library imports
import pymongo

# handling any location conflicts, if arises
import os   # if not used then we won't be able to properly deploy it on a linux server
import sys
current = os.path.dirname(os.path.realpath("db.py"))
parent = os.path.dirname(current)
sys.path.append(current)

# custom imports
from src.exception import CustomException
from src.logger import logging
from pymongo.server_api import ServerApi

# mongodb integration
class Crud:
    def __init__(self) -> None:
        # creating connection
        pass
    

    def insert(self, result:dict):
        try:
            connection = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.uhvvfup.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))
            db = connection["prediction_result"]
            collection = db["result_db"]

            collection.insert_one(result)

            logging.info("New entry inserted. Database Updated.")
        
        except Exception as e:
            logging.info("ERROR IN DATABASE INTEGRATION")
            raise CustomException(e, sys)