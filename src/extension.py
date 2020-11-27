import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
engine = create_engine(os.environ.get("POSTGRES_URL", "sqlite:///:memory:"), echo=True)
