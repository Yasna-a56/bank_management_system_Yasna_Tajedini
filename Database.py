from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# sqlite
DATABASE_URL = "sqlite:///database.db"

engine= create_engine(DATABASE_URL,echo=False, future=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine , autoflash=False, autocommit=False,future=True )


# helper
def get_session():

    return SessionLocal()

