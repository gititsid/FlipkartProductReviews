import os
import sys
import pandas as pd
from pymongo.mongo_client import MongoClient

from src.logger import logging
from src.exception import CustomException


def save_to_csv(reviews: list, filename):
    try:
        logging.info("saving reviews as csv")

        df = pd.DataFrame(reviews)
        os.makedirs("scrapped_review", exist_ok=True)
        filepath = os.path.join("scrapped_review", filename+".csv")
        
        df.to_csv(filepath, index=False)
        logging.info(f"saved reviews as csv at {filepath}")

    except Exception as e:
        logging.error("failed to save reviews as csv")
        raise CustomException(e, sys)
    

def push_to_mongodb(reviews: list):
    try:
        try:
            logging.info("Creating mongoDB client:")
            # upadte username and password here
            client = MongoClient("mongodb+srv://<username>:<password>@cluster0.90eolay.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
            if client.admin.command('ping'):
                logging.info("Pinged your deployment. You successfully connected to MongoDB!")

                db = client['flipkart_product_reviews']
                dataset = db['flipkart_product_reviews']
                
                logging.info("inserting reviews into: flipkart_product_reviews dataset")
                dataset.insert_many(reviews)
                logging.info(f"Loaded {len(reviews)} items to flipkart_product_reviews!")

        except Exception as e:
            logging.error("Couldn't establish mongoDB connection!")
            raise CustomException(e, sys)
        
        
    
    except Exception as e:
        logging.error('Failed to load data to flipkart_product_reviews dataset on mongoDB!')
        raise CustomException(e, sys)
