from fastapi import APIRouter

from app.api.endpoints import lead_router
from app.core.constants import LEAD_PREFIX, LEAD_TAGS

main_router = APIRouter()

main_router.include_router(
    router=lead_router, prefix=LEAD_PREFIX, tags=LEAD_TAGS
)
