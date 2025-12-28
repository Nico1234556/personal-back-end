from sqlmodel import SQLModel, create_engine, Session

# Se creará 'database.db' dentro de 'PERSONAL BACK-END'
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session