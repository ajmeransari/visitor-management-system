import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY= os.getenv("SECRET_KEY")# Replace with your actual secret key
    MYSQL_HOST=os.getenv("MYSQL_HOST")
    MYSQL_USER=os.getenv("MYSQL_USER")
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD") # Replace with your actual MySQL password
    MYSQL_DB=os.getenv("MYSQL_DB")