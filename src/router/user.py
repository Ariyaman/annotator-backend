from http import HTTPStatus
import bcrypt
import csv
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from database import get_db
from src.schemas.db_schemes import StatementSchema
from src.services.statement import get_statement_count_by_user_id_and_overall, get_statements_by_user_id_service
from src.services.user import create_user_service, get_user_by_email, get_user_by_id

from src.models.user import LoginUserBody, UserCreate


router = APIRouter()


@router.post("/signup")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_user_service(user, db)

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


@router.get("/get_marked_article_count_by_id/{user_id}")
def get_article_count_by_user_id(user_id: str, db: Session = Depends(get_db)):
    total_marked_article_count = get_statement_count_by_user_id_and_overall(db, user_id, True)

    return JSONResponse(jsonable_encoder({
        "count": total_marked_article_count
    }), HTTPStatus.OK)


@router.get("/get_statement_csv_by_id/{user_id}")
def get_statement_csv_by_user_id(user_id: str, db: Session = Depends(get_db)):
    try:
        statement_records = get_statements_by_user_id_service(db, user_id)
        user_record = get_user_by_id(user_id, db)

        csv_statement_name = f"{user_record.name}.csv"
        output_csv_file = open(csv_statement_name, "w")
        csv_output = csv.writer(output_csv_file)

        csv_output.writerow(StatementSchema.__table__.columns.keys())

        for statement in statement_records:

            if statement.sentence is None:
                statement.sentence = "*"

            if statement.company is None:
                statement.company = "*"

            csv_output.writerow([statement.statement_id, statement.overall, statement.emotion, statement.sentiment,
            statement.sentence, statement.company, statement.article_fk, statement.user_fk])

        output_csv_file.close()

        return FileResponse(csv_statement_name)
    except BaseException:
        return JSONResponse(jsonable_encoder({
            "msg": "Error while processing csv file"
        }), HTTPStatus.BAD_REQUEST)
