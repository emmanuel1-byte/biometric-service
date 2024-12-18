from pydantic import BaseModel, EmailStr, Field, field_validator
import base64


class Signup_Schema(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)
    public_key: str = None

    @field_validator("public_key")
    @classmethod
    def validate_pem_format(cls, v: str):
        print(v, ".....")
        if not v.startswith("-----BEGIN PUBLIC KEY-----\n"):
            raise ValueError('"Public key must start with -----BEGIN PUBLIC KEY-----"')
        if not v.endswith("-----END PUBLIC KEY-----\n"):
            raise ValueError("Public key must end with '-----END PUBLIC KEY-----'")

        # Ensure content is a valid base64 string
        try:
            content = (
                v.replace("-----BEGIN PUBLIC KEY-----", "")
                .replace("-----END PUBLIC KEY-----", "")
                .replace("\n", "")
                .strip()
            )
            print(content, "Base64 content.....")
            base64.b64decode(content, validate=True)
        except Exception as e:
            raise ValueError("Public key contains invalid Base64 content") from e

        return v

    class Config:
        form_attributes = True


class Login_Schema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)

    class Config:
        form_attributes = True


class Challenge_Schema(BaseModel):
    email: EmailStr
