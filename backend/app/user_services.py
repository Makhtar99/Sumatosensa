from typing import List
import logging
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from typing import  Optional


logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Users:
    async def createUser(self, username: str, email: str, password, role: str, session):
        try:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                user.email = email
                user.password_hash = pwd_context.hash(password)
            else:
                new_user = User(
                    username=username,
                    email=email,
                    password_hash=pwd_context.hash(password)
                )
                session.add(new_user)
            
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all_users(self, session: AsyncSession) -> List[User]:
        result = await session.execute(select(User))
        return result.scalars().all()

    async def update_user(self, session: AsyncSession, user_id: int, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
        user = await self.get_user_by_id(session, user_id)
        if not user:
            return None

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password_hash = pwd_context.hash(password)

        try:
            await session.commit()
            await session.refresh(user)
            logger.info(f"Utilisateur ID={user_id} mis à jour.")
            return user
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Erreur lors de la mise à jour de l'utilisateur : {e}")
            raise

    async def delete_user(self, session: AsyncSession, user_id: int) -> bool:
        user = await self.get_user_by_id(session, user_id)
        if not user:
            return False

        try:
            await session.delete(user)
            await session.commit()
            logger.info(f"Utilisateur ID={user_id} supprimé.")
            return True
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Erreur lors de la suppression de l'utilisateur : {e}")
            raise