import random
from datetime import datetime, timedelta

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlmodel import Session

from models.user import User
from repositorys.userRepository import UserRepository
from services.BrevoService import BrevoService
from shemats.shemats import UserInput, UserOutput


class UserService:
    def __init__(self, db: Session):
        self.userRepository = UserRepository(db)
        self.brevoService = BrevoService()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.generate_validation_code = random.randint(100000, 999999)  # Générer un code à 6 chiffres

    # create user and verify email
    def createUser(self, userInput: UserInput):
        exist = self.EmailIsExist(userInput.email)
        if not exist:
            raise HTTPException(status_code=400, detail="Email already exists")
        validation_code = self.generate_validation_code
        expiration_time = datetime.utcnow() + timedelta(minutes=15)
        user = User(**userInput.model_dump(exclude_none=True))
        user.hashed_password = self.pwd_context.hash(user.hashed_password)
        user.validation_code = validation_code
        user.validation_code_expires_at = expiration_time
        self.userRepository.createUser(user)
        # if self.userRepository.createUser(user):
        # self.brevoService.send_mail(
        #     user.email,
        #     "Votre code de validation",
        #     f"Votre code de validation est : {user.validation_code}"
        # )

        return UserOutput(name=user.name, email=user.email)

    def EmailIsExist(self, email: str):
        user = self.userRepository.getUserByEmail(email)
        if user and user.email:
            return False
        return True

    def get_user_by_id(self, user_id: int):
        if not self.userRepository.get_user_by_id(user_id):
            raise HTTPException(status_code=404, detail=f"user  not found")
        return self.userRepository.get_user_by_id(user_id)


