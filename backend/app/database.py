'''Singleton class for the database connection'''

import os
from dotenv import load_dotenv
from pymongo import MongoClient

# singleton

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB", "ProjecTrack_dev")

class Database:
    '''Singleton class for the database connection'''
    _instance = None
    client = None
    db = None

    def __new__(cls):
        '''Creates the singleton instance'''
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)   # Creates the instance
            cls._instance.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)   # Connects to the database
            cls._instance.db = cls._instance.client[MONGO_DB_NAME]

        return cls._instance

    def __del__(self):
        '''Closes the connection safely'''
        if getattr(self, 'client', None) is not None:
            try:
                self.client.close()
            except Exception:
                pass
        self._instance = None
        self.client = None
        self.db = None


def get_db():
    '''Method that obtains the database instance from anywhere within the system'''
    return Database().db
