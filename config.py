import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DB = 'form'
