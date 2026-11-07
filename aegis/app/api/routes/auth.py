from fastapi import APIRouter, status, Depends, HTTPException
from app.api.schemas.auth import RegisterRequest, UserResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_session
from app.application.exceptions import EmailAlreadyRegistered
from app.application.register_user import RegisterUser, RegisterUserCommand
from app.infra.repository.user_repository import UserRepository

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: RegisterRequest, session: AsyncSession = Depends(get_session)) -> UserResponse:
    repository = UserRepository(session=session)
    use_case = RegisterUser(repository=repository)

    command = RegisterUserCommand(email=request.email, password=request.password, tenant_id=request.tenant_id)

    try:
        user = await use_case.register(command=command)
    except EmailAlreadyRegistered:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email Already registered"
        )

    await session.commit()

    return UserResponse(
        user_id=user.user_id,
        email=user.email,
        tenant_id=user.tenant_id,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )