import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


def validate_jwt(token: str):
    try:
        decoded_jwt = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return decoded_jwt

    except ExpiredSignatureError as e:
        print(f"Expired token:{e}")
        raise HTTPException(status_code=401, detail={"message": "Expired token"})

    except InvalidTokenError as e:
        print(f"Invalid token error: {e}")
        raise HTTPException(status_code=400, detail={"message": "Invalid token"})

    except Exception:
        raise


def create_access_token(user_id: str):
    encoded_jwt = jwt.encode(
        {"sub": user_id, "exp": datetime.now(tz=timezone.utc) + timedelta(days=60)},
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    return encoded_jwt
