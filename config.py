from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    """Configuration file"""
    HOST: str = os.getenv("HOST")
    USER: str = os.getenv("USER")
    PORT: str = os.getenv("PORT")
    DBNAME: str = os.getenv("DBNAME")
    PASSWORD: str = os.getenv("PASSWORD")
    SSLMODE: str = os.getenv("SSLMODE")
    URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
