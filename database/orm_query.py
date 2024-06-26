from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Data


async def orm_add_topic(session: AsyncSession, data: dict, chat_id=int):
    obj = Data(
        id_user=chat_id,
        open_mic_topic=data["data_name"],
    )
    session.add(obj)
    await session.commit()


async def orm_get_topic(session: AsyncSession):
    query = select(Data)
    result = await session.execute(query)
    return result.scalars().all()
