from fastapi import APIRouter, status

from app.core.enums import ApiTagEnum

router = APIRouter(tags=[ApiTagEnum.HEALTH_CHECK], prefix="/health_check")


@router.get("")
async def perform_healthcheck():
    return status.HTTP_200_OK
