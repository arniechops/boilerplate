from abc import ABC, abstractmethod

from app.models.health import HealthStatus


class AbstractHealthRepository(ABC):
    @abstractmethod
    async def get_status(self) -> HealthStatus: ...


class HealthRepository(AbstractHealthRepository):
    async def get_status(self) -> HealthStatus:
        return HealthStatus(status="ok", version="0.1.0")
