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

All config lives in `src/app/config.py` as a pydantic-settings `Settings` class. Never use `os.getenv()` directly elsewhere in the codebase.

To add a new variable, add a field to `Settings`:
```python
# Required — app will refuse to start if missing from the environment
database_url: str

# Optional — has a fallback default
some_flag: bool = False
```

Then add the value to `.env` for local development (this file is gitignored and never committed):
```env
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
```

Access config anywhere via the singleton:
```python
from app.config import settings

settings.database_url
```

In production, set the same names as real environment variables on the host — pydantic-settings reads env vars first, then falls back to `.env`.

## Bespoke scripts

One-off scripts live in `scripts/`. Run from the `api/` directory:

```bash
just script <name>        # runs scripts/<name>.py
uv run scripts/<name>.py  # equivalent
```

### Two modes

**Default — uses the project venv.**
No metadata block. Project packages are importable (`from app.config import settings`).

```python
#!/usr/bin/env -S uv run
from app.config import settings

def main() -> None:
    ...
```

**Extra deps — uses an isolated environment.**
Add a [PEP 723](https://peps.python.org/pep-0723/) inline metadata block to pull in packages not in `pyproject.toml`. This runs in isolation, so project packages are no longer importable — choose one model or the other.

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx",
# ]
# ///
```

### Which mode to use

- **Script needs project code** (`from app.X import ...`) → default mode. If it also needs an extra package, add that package to `pyproject.toml` via `uv add` rather than using the PEP 723 block.
- **Script is truly standalone** with no need for project code, and its extra dep would pollute `pyproject.toml` (e.g. a one-off data migration tool, a webhook tester) → PEP 723 mode. To still access project code in this mode, declare the local package in the block:

```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx",
#   "api @ ..",  # installs the local api package into the isolated env
# ]
# ///
```

(`..` is relative to `scripts/`, pointing up to `api/` where `pyproject.toml` lives.)

## Dependency management

```bash
uv add <package>          # add a runtime dependency
uv add --dev <package>    # add a dev dependency
uv remove <package>       # remove a dependency
```

Never edit `uv.lock` by hand.
