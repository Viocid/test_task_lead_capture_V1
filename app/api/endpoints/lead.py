from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.lead import lead_crud
from app.schemas.lead import LeadCreate, LeadDB

router = APIRouter()


@router.post("/", response_model=LeadDB, status_code=201)
async def create_lead(
    lead: LeadCreate,
    session: AsyncSession = Depends(get_async_session),
):
    return await lead_crud.create(lead, session)


@router.get("/", response_model=list[LeadDB])
async def get_leads(
    session: AsyncSession = Depends(get_async_session),
):
    return await lead_crud.get_multi(session)
