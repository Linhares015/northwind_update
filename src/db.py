import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import warnings
from sqlalchemy.exc import SAWarning

warnings.filterwarnings(
    "ignore",
    "Did not recognize type 'bpchar'",
    category=SAWarning
)

load_dotenv()

DB_URL = os.getenv(
    "DB_URL",
    "postgresql://northwind:sua_senha_segura@localhost:5432/northwind"
)

engine = create_engine(DB_URL)
metadata = MetaData()

# se quiser refletir tudo de uma vez:
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
