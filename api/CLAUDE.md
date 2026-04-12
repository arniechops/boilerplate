# API — Build Guide

## Stack
- **Runtime**: Python 3.13, managed by [UV](https://docs.astral.sh/uv/)
- **Framework**: FastAPI
- **Config**: pydantic-settings (reads `.env` + environment variables)
- **Source root**: `src/app/` — all application code lives here

## Running the server
```bash
just dev     # hot-reload (development)
just start   # production
```

## Architecture — Onion / Clean Architecture

Every feature is split across four layers. Dependencies only point **inward** — outer layers may import from inner layers, never the reverse.

```
routers → use_cases → repositories → models
```

### Layer responsibilities

| Layer | Directory | Rule |
|---|---|---|
| **Models** | `src/app/models/` | Pure Pydantic domain entities. No imports from other app layers. |
| **Repositories** | `src/app/repositories/` | Data access only. Define an `Abstract*Repository` ABC and a concrete implementation. Use cases depend on the ABC, not the concrete class. |
| **Use Cases** | `src/app/use_cases/` | One class per operation (e.g. `GetHealthStatus`). Receives repository via `__init__`. Contains all business logic. No FastAPI imports. |
| **Routers** | `src/app/routers/` | Thin HTTP layer. Instantiates the use case with its concrete repository and calls `.execute()`. No business logic here. |

### Adding a new feature — checklist

1. **Model** — add a Pydantic class in `src/app/models/<feature>.py`
2. **Repository** — add `Abstract<Feature>Repository` (ABC) and a concrete implementation in `src/app/repositories/<feature>.py`
3. **Use case** — add a class in `src/app/use_cases/<feature>.py` that takes the abstract repository in `__init__` and exposes an `execute()` method
4. **Router** — add a `router = APIRouter(...)` in `src/app/routers/<feature>.py`, wire the concrete repository into the use case
5. **Register** — call `app.include_router(...)` in `src/app/main.py`

### Example flow (health check)
```
GET /api/v1/health
  → routers/health.py        # validates HTTP, calls use case
  → use_cases/health.py      # business logic (none here, but this is where it lives)
  → repositories/health.py   # fetches data
  → models/health.py         # HealthStatus entity returned up the chain
```

## Configuration

All config lives in `src/app/config.py` as a pydantic-settings `Settings` class. Add new config fields there — never use `os.getenv()` directly elsewhere. Values are read from environment variables and `.env` (in the working directory when the server starts).

## Dependency management

```bash
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a dev dependency
uv remove <package>       # remove a dependency
```

Never edit `uv.lock` by hand.
