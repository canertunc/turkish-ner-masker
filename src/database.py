import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    def __init__(self, db_type="main"):
        self.db_type = db_type
        self.connection = None
        
    def connect(self):
        try:
            if self.db_type == "main":
                self.connection = psycopg2.connect(
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
            else:  # training
                self.connection = psycopg2.connect(
                    dbname=os.getenv("TRAINING_DB_NAME"),
                    user=os.getenv("TRAINING_DB_USER"),
                    password=os.getenv("TRAINING_DB_PASSWORD"),
                    host=os.getenv("TRAINING_DB_HOST"),
                    port=os.getenv("TRAINING_DB_PORT")
                )
            return self.connection
        except psycopg2.OperationalError as e:
            print(f"Connection failed: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def get_training_data():
    """Get training data from the training database"""
    with DatabaseConnection("training") as db:
        if db.connection:
            query = 'SELECT * FROM "ArizaV1TrainingDataset";'
            return pd.read_sql_query(query, db.connection)
    return None

def get_people_data():
    """Get people data from the main database"""
    with DatabaseConnection("main") as db:
        if db.connection:
            query = 'SELECT * FROM "Common_People";'
            return pd.read_sql_query(query, db.connection)
    return None 