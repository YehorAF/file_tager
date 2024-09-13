import dotenv
import os

dotenv.load_dotenv()

OS = os.getenv("OS")
MONGODB_URL = os.getenv("MONGODB_URL")
MONGODB_NAME = os.getenv("MONGODB_NAME")