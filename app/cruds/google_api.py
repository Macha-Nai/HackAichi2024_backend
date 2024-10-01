import secrets
from urllib.parse import urlencode
from fastapi.responses import RedirectResponse
import requests
from fastapi import HTTPException
from .. import env

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
]


def auth():
    state = secrets.token_urlsafe(16)
    params = {
        "client_id": env.GOOGLE_CLIENT_ID,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "redirect_uri": env.REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    auth_url = f"{env.AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    response = RedirectResponse(url=auth_url)
    return response


def get_access_token(code: str) -> dict:
    data = {
        "code": code,
        "client_id": env.GOOGLE_CLIENT_ID,
        "client_secret": env.GOOGLE_CLIENT_SECRET,
        "redirect_uri": env.REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(env.TOKEN_URL, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="アクセストークンの取得に失敗しました。")

    return response.json()


def set_cookies(code: str):
    token_data = get_access_token(code)
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")
    expires_in = token_data.get("expires_in")
    token_type = token_data.get("token_type")
    response = RedirectResponse(url="http://localhost:5173/")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
    )
    return response
