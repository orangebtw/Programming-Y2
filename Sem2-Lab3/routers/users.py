from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from models.user import User
from schemas.user import UserCreateSchema, UserUpdateSchema, UserSchema
from database import get_db_session

router = APIRouter()

@router.get("/")
async def user_list(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.post("/")
async def create_user(user: UserCreateSchema, response: Response, session: AsyncSession = Depends(get_db_session)):
    session.add(User(username=user.username, email=user.email))
    try:
        await session.commit()
        response.status_code = status.HTTP_201_CREATED
        return "success"
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "User with this id already exists")

@router.get("/{user_id}")
async def user_by_id(user_id: int, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    try:
        user = result.scalar_one()
        schema = UserSchema.model_validate(user)
        return schema
    except NoResultFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

@router.put("/{user_id}")
async def update_user_by_id(user_id: int, schema: UserUpdateSchema, session: AsyncSession = Depends(get_db_session)):
    if schema.username is None and schema.email is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username or email must not be null")

    result = await session.execute(select(User).where(User.id == user_id))
    try:
        user = result.scalar_one()
        if schema.email is not None:
            user.email = schema.email
        if schema.username is not None:
            user.username = schema.username
        await session.commit()
        return "success"
    except NoResultFound:
        return HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
        

@router.delete("/{user_id}")
async def delete_user_by_id(user_id: int, session: AsyncSession = Depends(get_db_session)):
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
    return "success"
