from sqlmodel import Session, SQLModel, create_engine
from pydantic import BaseModel

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False} #forcing py to use multiple threads
engine = create_engine(sqlite_url, connect_args=connect_args) #connect with DB

# Function to create the database and tables
def create_db_and_tables():
    # This is imported here to avoid circular dependency issues
    SQLModel.metadata.create_all(engine)

# Dependency function to get a database session
def get_session():
    with Session(engine) as session:
        yield session