# app/services/auth_service.py
import jwt
from fastapi import Request, HTTPException
from app.core.config import settings


class AuthService:
    @staticmethod
    def get_user_id_from_cookie(request: Request) -> str:
        # 1. 자바 JwtAuthenticationFilter에서 정의한 쿠키 이름 "accessToken"
        token = request.cookies.get("accessToken")

        if not token:
            raise HTTPException(status_code=401, detail="인증 쿠키가 없습니다.")

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=["HS384"]
            )
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="토큰에 유저 식별 정보가 없습니다.")

            return str(user_id)

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="토큰 기한이 만료되었습니다.")
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=401, detail="토큰 서명이 일치하지 않습니다.")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.")