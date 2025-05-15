import os
from dotenv import load_dotenv

load_dotenv()

VT_API_KEY = os.getenv("VT_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./virustotal.db")
CACHE_TTL = 300