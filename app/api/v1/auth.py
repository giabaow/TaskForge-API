from fastapi import APIRouter, status
from app.api.deps import DBSession
from app.core.security import create_access_token
from app.schemas import LoginRequest, Token, UserCreate, UserRead
from app.services import services

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: DBSession):
    return await services.register_user(db, data.email, data.password, data.full_name)


@router.post("/login", response_model=Token)
async def login(data: LoginRequest, db: DBSession):
    user = await services.authenticate(db, data.email, data.password)
    return Token(access_token=create_access_token(str(user.id)))
