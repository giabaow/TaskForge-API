from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import get_settings
from app.db.session import get_db
from app.models import User

bearer = HTTPBearer(auto_error=False)
DBSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    db: DBSession, credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]
) -> User:
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token", headers={"WWW-Authenticate": "Bearer"})
    if not credentials: raise unauthorized
    try:
        payload = jwt.decode(credentials.credentials, get_settings().jwt_secret_key, algorithms=[get_settings().jwt_algorithm])
        user_id = int(payload.get("sub", ""))
    except (jwt.PyJWTError, ValueError, TypeError):
        raise unauthorized
    user = await db.get(User, user_id)
    if not user: raise unauthorized
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
