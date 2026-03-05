from fastapi import APIRouter, Depends  
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from models.user import User
from schemas.response import ResponseSchema, ErrorSchema
from schemas.user import UserCreateSchema, UserUpdateSchema, UserSchema
from database import get_db_session

router = APIRouter()

@router.get("/")
async def user_list(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.post("/")
async def create_user(user: UserCreateSchema, session: AsyncSession = Depends(get_db_session)):
    session.add(User(username=user.username, email=user.email))
    try:
        await session.commit()
        return ResponseSchema(success=True, error=ErrorSchema(message="User added successfully"))
    except IntegrityError:
        await session.rollback()
        return ResponseSchema(success=False, error=ErrorSchema(message="User already exists"))

@router.get("/{user_id}")
async def user_by_id(user_id: int, session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    try:
        user = result.scalar_one()
        schema = UserSchema.model_validate(user)
        return ResponseSchema(success=True, data=schema)
    except NoResultFound:
        return ResponseSchema(success=False, error=ErrorSchema(message="User not found"))

@router.put("/{user_id}")
async def update_user_by_id(user_id: int, schema: UserUpdateSchema, session: AsyncSession = Depends(get_db_session)):
    if schema.username is None and schema.email is None:
        return ResponseSchema(success=False, error=ErrorSchema(message="Nothing to update"))

    result = await session.execute(select(User).where(User.id == user_id))
    try:
        user = result.scalar_one()
        if schema.email is not None:
            user.email = schema.email
        if schema.username is not None:
            user.username = schema.username
        await session.commit()
        return ResponseSchema(success=True)
    except NoResultFound:
        return ResponseSchema(success=False, error=ErrorSchema(message="User not found"))
        

@router.delete("/{user_id}")
async def delete_user_by_id(user_id: int, session: AsyncSession = Depends(get_db_session)):
    await session.execute(delete(User).where(User.id == user_id))
    await session.commit()
    return ResponseSchema(success=True, error=ErrorSchema(message="User deleted successfully"))
