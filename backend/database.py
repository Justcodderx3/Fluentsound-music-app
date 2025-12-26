from sqlalchemy import Column, String, Integer, create_engine, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

DataBase_URL = "sqlite:///./tracks.db"
engine = create_engine(
    DataBase_URL,
    connect_args={"check_same_thread": False},
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class TrackDB(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    artist_name = Column(String(200), nullable=True)
    track_name = Column(String(200), nullable=False)
    file_path = Column(String, nullable=False, unique=True)
    file_format = Column(String(10), nullable=False)
    add_date = Column(DateTime, default=datetime.now)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
