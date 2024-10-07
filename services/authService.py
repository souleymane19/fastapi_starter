import random
from datetime import timedelta, datetime

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session
from starlette import status

from confing.db import get_db
from models.user import User
from repositorys.userRepository import UserRepository
from services.userService import UserService
from shemats.shemats import UserInput


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
        self.user_service = UserService(db)
        self.SECRET_KEY = "SECRET_KEY_RANDOM_GENERATE_IT"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))
        # Fonction pour vérifier un mot de passe

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate(self, username: str, password: str):
        get_user = self.user_repository.getUserByEmail(username)
        if not get_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect email or password",
                                headers={"WWW-Authenticate": "Bearer"},

                                )
        if not self.verify_password(password, get_user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Incorrect email or password",
                                headers={"WWW-Authenticate": "Bearer"},

                                )

        data = {"sub": get_user.email}
        return self.create_access_token(data)
        # Function to createtoken JWT

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        SECRET_KEY = self.SECRET_KEY
        ALGORITHM = self.ALGORITHM
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

        # Dépendance pour récupérer l'utilisateur à partir du token

    async def get_current_user(self):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Correction: ne pas passer `self` comme argument à `jwt.decode`
            SECRET_KEY = "SECRET_KEY_RANDOM_GENERATE_IT"
            ALGORITHM = "HS256"
            payload = jwt.decode(self.token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        # Utilise la méthode correcte pour récupérer l'utilisateur

        user = UserRepository(self.db).getUserByEmail(email)
        if user is None:
            raise credentials_exception
        return user

        # cette fonction permet de rechercher l'utilisateur
        # et valité le code envoyé

    def validate_user_code(self, user_id: int, validation_code: str):
        if self.is_active_user(user_id):
            raise HTTPException(status_code=400, detail="User is active")
        user_by_id = self.user_service.get_user_by_id(user_id)
        if not user_by_id:
            raise HTTPException(status_code=404, detail=f"email {user_id} not found")
        if user_by_id.validation_code != validation_code:
            raise HTTPException(status_code=400, detail="Code de validation incorrect")

        if datetime.utcnow() > user_by_id.validation_code_expires_at:
            raise HTTPException(status_code=400, detail="Code de validation expiré")

        return self.activate_user(user_by_id)

    # cette fonction permet d'activé
    def activate_user(self, user:User):
        user.is_active=True
        remove_user = User()
        user.validation_code=remove_user.validation_code
        user.validation_code_expires_at=remove_user.validation_code_expires_at
        self.user_repository.activate_user(user)
        return {"active": True}

    def is_active_user(self, user_id) -> bool:
        if self.user_service.get_user_by_id(user_id).is_active:
            return True
        return False
