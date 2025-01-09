import dotenv
import os

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
NPOINT = os.getenv("NPOINT")