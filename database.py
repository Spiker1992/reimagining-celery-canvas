from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

# SQLAlchemy setup for SQLite
SQLITE_DB_URL = 'sqlite:///workflow.db'
engine = create_engine(SQLITE_DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Example table definition
class WorkflowLog(Base):
	__tablename__ = 'workflow_log'
	id = Column(Integer, primary_key=True, index=True)
	workflow_id = Column(String, index=True)
	timestamp = Column(DateTime, default=datetime.datetime.utcnow)
	payload = Column(String)

# Create tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()