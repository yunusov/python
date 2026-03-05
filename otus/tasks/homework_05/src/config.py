import os
from dotenv import load_dotenv
from pathlib import Path

from src.models import PhoneDictionary, Storage

load_dotenv()
MIDDLEWARE_SECRET_KEY = os.getenv("MIDDLEWARE_SECRET_KEY")
SERVER_IP = os.getenv("SERVER_IP")
str_server_port = os.getenv("SERVER_PORT")
SERVER_PORT = int(str_server_port)
SERVER_URL = "http://" + SERVER_IP + ":" + str_server_port

parent_folder = Path(__file__).parent
storage = Storage(parent_folder)
phone_dict = PhoneDictionary(storage)