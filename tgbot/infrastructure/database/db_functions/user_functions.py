from sqlalchemy import select, update, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from tgbot.infrastructure.database.db_models.user_models import User


async def add_user(session: AsyncSession, telegram_id: int, role='user'):
    insert_stmt = select(
        User
    ).from_statement(
        insert(
            User
        ).values(
            telegram_id=telegram_id,
            role=role
        ).returning(User).on_conflict_do_nothing()
    )
    result = await session.scalars(insert_stmt)
    return result.first()


async def get_user(session: AsyncSession, telegram_id: int) -> User:
    stmt = select(User).where(User.telegram_id == telegram_id)
    result: AsyncResult = await session.scalars(stmt)
    return result.first()


async def get_some_users(session: AsyncSession, *clauses) -> list[User]:
    stmt = select(User).where(*clauses).order_by(User.created_at.desc())
    result: AsyncResult = await session.scalars(stmt)
    return result.unique().all()


async def get_users_count(session: AsyncSession, *clauses) -> int:
    stmt = select(func.count(User.telegram_id)).where(*clauses)
    result: AsyncResult = await session.scalar(stmt)
    return result


async def update_user(session: AsyncSession, *clauses, **values):
    stmt = update(User).where(*clauses).values(**values)
    await session.execute(stmt)


# async def reset_all_users_schedulers(session: AsyncSession):
#     users = await get_some_users(session=session)
#     if users:
#         for user in users:
#             await update_user_search_status(session=session, telegram_id=user.telegram_id, search_status="off")
#             await update_user_scheduler_job_id(session=session, telegram_id=user.telegram_id)
#             await update_user_interval_companion_id(session=session, telegram_id=user.telegram_id)
#             await session.commit()
#         return 0
#     return -1
