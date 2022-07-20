from http import HTTPStatus
from http.client import HTTPException
from uuid import uuid4
import bcrypt
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from fastapi.encoders import jsonable_encoder

from src.models.user import Gender, LoginUserBody, Roles, UserCreate
from src.schemas.db_schemes import UserSchema


router = APIRouter()

@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hashpw(str(user.password).encode("utf-8"), bcrypt.gensalt())
    db_user = UserSchema(
        user_id = str(uuid4()),
        name = user.name,
        email = user.email,
        hashed_password = hashed_password,
        gender = Gender[user.gender].name,
        role = Roles.user.name,
        age = user.age,
        profession = user.profession
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login")
def login(user: LoginUserBody, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    selected_user = db.query(UserSchema).filter(UserSchema.email == email).first()

    if(bcrypt.checkpw(str(password).encode("utf-8"), str(selected_user.hashed_password).encode("utf-8"))):
        return jsonable_encoder(
            {
                "role": selected_user.role,
                "user_id": selected_user.user_id,
                "status": {
                    "status_code": HTTPStatus.OK
                }
            }
        )
    else:
        return jsonable_encoder(
            {
                "status": HTTPException(HTTPStatus.UNAUTHORIZED, "Unauthorized")
            }
        )