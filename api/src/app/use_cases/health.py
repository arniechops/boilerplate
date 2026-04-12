from app.models.health import HealthStatus
from app.repositories.health import AbstractHealthRepository


class GetHealthStatus:
    def __init__(self, repository: AbstractHealthRepository) -> None:
        self._repository = repository

    async def execute(self) -> HealthStatus:
        return await self._repository.get_status()
