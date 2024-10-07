import os
from dotenv import load_dotenv
# Charger le fichier .env

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from confing.db import get_db
from services.BrevoService import BrevoService
from services.authService import AuthService
from services.userService import UserService
from shemats.shemats import UserInput

router = APIRouter()


#
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
#
#
# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
#
#
@router.post("/users/")
async def create_user(
        data: UserInput, db: Session = Depends(get_db)

):
    _service = UserService(db)
    return _service.createUser(data)


# @router.get("/users/", response_model=UserOutput)
# async def getUserAuth(
#         username: str, password: str, db: Session = Depends(get_db)
#
# ):
#     _service = AuthService(db)
#     return _service.authenticate(username, password)

@router.get("/send")
async def sendEmail():
    service = BrevoService()
    service.send_mail(
        to_email="souleymane14131@gmail.com",
        subject="Is Python SDK work done?",
        text_content="Hi Sourabh,\nIs Python SDK work complete or not?")

    return {"message": os.getenv("EMAIL_FROM")}


@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.authenticate(form_data.username, form_data.password)


@router.post("/validate")
def validate_user_code(user_id: int, codes: str, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.validate_user_code(user_id, codes)
