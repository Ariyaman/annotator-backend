from uuid import uuid4
import bcrypt
from sqlalchemy.orm import Session

from src.models.user import Gender, Roles, UserCreate
from src.schemas.db_schemes import UserSchema


def create_user_service(user: UserCreate, db: Session):
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

def get_user_by_email(email: str, db: Session):
    return db.query(UserSchema).filter(UserSchema.email == email).first()