from fastapi import APIRouter, HTTPException
from .schema import Signup_Schema, Login_Schema, Challenge_Schema
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from ...utils.database import SessionDep
from . import repository
from ...helpers.key import create_challenge_token
from ...helpers.key import validate_signatures
from ...helpers.hashing import hash_password, compare_password
from ...helpers.token import create_access_token


auth = APIRouter(prefix="/api/auth", tags=["Authentication"])


@auth.post("/signup", responses={409: {}})
def signup(validated_data: Signup_Schema, session: SessionDep):
    existing_user = repository.find_user_by_email(validated_data.email, session)
    if existing_user:
        raise HTTPException(
            status_code=409, detail={"message": "Account already exist"}
        )

    validated_data.password = hash_password(validated_data.password)
    new_user = repository.create_user(validated_data, session)

    return JSONResponse(
        content={
            "message": "Account created",
            "data": new_user.model_dump(mode="json", exclude=["password"]),
        }
    )


@auth.post("/challenge", responses={404: {}})
def get_challenge(validated_data: Challenge_Schema, session: SessionDep):
    user = repository.find_user_by_email(validated_data.email, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    challenge = create_challenge_token()

    return JSONResponse(content={"data": challenge}, status_code=201)


@auth.get("/verify", responses={404: {}, 401: {}, 400: {}})
def validate_key_signatures(
    email: EmailStr, signature: str, challenge: str, session: SessionDep
):
    user = repository.find_user_by_email(email, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    is_valid = validate_signatures(challenge, signature, user.public_key)

    if not is_valid:
        raise HTTPException(status_code=401, detail={"message": "Invalid signature"})

    access_token = create_access_token(user.id)
    return JSONResponse(
        content={"data": {"access_token": access_token}}, status_code=200
    )


@auth.post("/login", responses={404: {}, 401: {}})
def login(validated_data: Login_Schema, session: SessionDep):
    user = repository.find_user_by_email(validated_data.email, session)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    is_valid_password = compare_password(validated_data.password, user.password)
    if not is_valid_password:
        raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

    access_token = create_access_token(user.id)
    return JSONResponse(
        content={"data": {"access_token": access_token}}, status_code=200
    )
