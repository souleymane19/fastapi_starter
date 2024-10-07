from sqlmodel import Field, Session, SQLModel, create_engine

mysql_url = f"mysql+pymysql://root@localhost:3306/dev"

engine = create_engine(mysql_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# def get_db():
#     """
#     Create a database session.
#     Yields:
#         Session: The database session.
#     """
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

def get_db():
    with Session(engine) as session:
        yield session
