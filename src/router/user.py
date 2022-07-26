from http import HTTPStatus
import bcrypt
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db
from src.services.article import set_articles
from src.services.user import create_user_service, get_user_by_email, get_user_by_id

from src.models.user import LoginUserBody, UserCreate


router = APIRouter()


@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user_service(user, db)
    set_articles(db, user.user_id)

    return JSONResponse(jsonable_encoder({"msg": "User created"}), HTTPStatus.CREATED)


@router.post("/login")
def login(user: LoginUserBody, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    selected_user = get_user_by_email(email, db)

    if(selected_user is None):
        return JSONResponse(content=jsonable_encoder({
            "msg": "User not found"
        }),
            status_code=HTTPStatus.NOT_FOUND
        )
    elif(bcrypt.checkpw(str(password).encode("utf-8"), str(selected_user.hashed_password).encode("utf-8"))):
        response = JSONResponse(content=jsonable_encoder({
            "user_id": selected_user.user_id,
        }),
            status_code=HTTPStatus.OK
        )

        response.set_cookie("annotatorUserId", selected_user.user_id, expires=2592000)
        return response
    else:
        return JSONResponse(content=jsonable_encoder({
            "msg": "User not authorized"
        }),
            status_code=HTTPStatus.UNAUTHORIZED
        )


@router.get("/get_role_by_id/{user_id}")
def get_role_by_id(user_id: str, db: Session = Depends(get_db)):
    selected_user = get_user_by_id(user_id, db)

    if(selected_user is None):
        return JSONResponse(jsonable_encoder({
            "msg": "User not found"
            }),
            status_code=HTTPStatus.NOT_FOUND
        )
    else:
        return JSONResponse(jsonable_encoder({
            "role": selected_user.role,
            "name": selected_user.name
        }))
