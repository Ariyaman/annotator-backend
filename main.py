from http import HTTPStatus
from uuid import uuid4
import bcrypt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from database import Base, SessionLocal, engine
from src.models.user import Gender, LoginUserBody, Roles, UserCreate
from src.schemas.db_schemes import UserSchema

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.post("/signup")
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

@app.post("/login")
def login(user: LoginUserBody, db: Session = Depends(get_db)):
    email = user.email
    password = user.password

    selected_user = db.query(UserSchema).filter(UserSchema.email == email).first()

    if(bcrypt.checkpw(str(password).encode("utf-8"), str(selected_user.hashed_password).encode("utf-8"))):
        return jsonable_encoder(
            {
                "role": selected_user.role,
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