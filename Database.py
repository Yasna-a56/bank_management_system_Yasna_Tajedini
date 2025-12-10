from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# mysql
DATABASE_URL = "sqlite:///database.db"

engine= create_engine(DATABASE_URL,echo=False, future=True)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine , autoflush=False, autocommit=False,future=True )

# helper
def get_session():

    return SessionLocal()

