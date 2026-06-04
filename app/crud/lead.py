from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.lead import Lead


class CRUDLead(CRUDBase):

    async def get_multi(self, session: AsyncSession) -> list[Lead]:
        db_objs = await session.execute(
            select(self.model).order_by(self.model.create_date.desc())
        )
        return db_objs.scalars().all()


lead_crud = CRUDLead(Lead)
