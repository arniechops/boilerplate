from fastapi import APIRouter

from app.models.health import HealthStatus
from app.repositories.health import HealthRepository
from app.use_cases.health import GetHealthStatus

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthStatus)
async def health_check() -> HealthStatus:
    use_case = GetHealthStatus(repository=HealthRepository())
    return await use_case.execute()
