from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import Session, select

from models.user import User
from shemats.shemats import UserInput, UserOutput


class UserRepository:
    def __init__(self, db: Session):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.db = db

    def createUser(self, user: User):
        self.db.add(user)
        self.db.commit()
        return user

    def getUserByEmailAndPassword(self, email, password):
        statement = select(User).where((User.email == email) & (User.hashed_password == password))
        user = self.db.scalar(statement)
        return user

    def getUserByEmail(self, email):
        statement = select(User).where(User.email == email)
        user = self.db.scalar(statement)
        return user

    def getUser(self, user):
        statement = (select(User)
                     .where((User.email == user.email) & (User.hashed_password == user.hashed_password)))
        return self.db.scalar(statement).one_or_none()

    def updateUser(self, id_user: int, user):
        statement = (select(User).where(User.id == id_user))
        scalar = self.db.scalar(statement)
        scalar.name = user.name
        scalar.email = user.email
        self.db.add(user)
        self.db.commit()
        return scalar

    def activate_user(self, user):
        self.db.add(user)
        self.db.commit()

    def get_user_by_id(self, user_id: int):
        statement = select(User).where(User.id == user_id)
        user = self.db.scalar(statement)
        return user
