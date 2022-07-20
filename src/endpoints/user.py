from http import HTTPStatus
from http.client import NOT_FOUND
import bcrypt
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from src.data.user import create_user_service, get_user_by_email, get_user_by_id

from src.models.user import LoginUserBody, UserCreate


router = APIRouter()


@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    create_user_service(user, db)

    return JSONResponse({"status": {"status_code": HTTPStatus.CREATED}})


@router.post("/login")
def login(user: LoginUserBody, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    selected_user = get_user_by_email(email, db)

    if(selected_user is None):
        return JSONResponse(content={
            "msg": "User not found"
        },
            status_code=HTTPStatus.NOT_FOUND
        )
    elif(bcrypt.checkpw(str(password).encode("utf-8"), str(selected_user.hashed_password).encode("utf-8"))):
        response = JSONResponse(content={
            "role": selected_user.role,
            "user_id": selected_user.user_id,
            "msg": "User created"
        },
            status_code=HTTPStatus.CREATED
        )

        response.set_cookie("annotatorUserId", selected_user.user_id, expires=2592000)
        return response
    else:
        return JSONResponse(content={
            "msg": "User not authorized"
        },
            status_code=HTTPStatus.UNAUTHORIZED
        )


@router.get("/get_role_by_id/{user_id}")
def get_role_by_id(user_id: str, db: Session = Depends(get_db)):
    selected_user = get_user_by_id(user_id, db)

    if(selected_user is None):
        return JSONResponse({
            "msg": "User not found"
            },
            status_code=HTTPStatus.NOT_FOUND
        )
    else:
        return JSONResponse({
            "role": selected_user.role
        })
