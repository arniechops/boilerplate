#!/usr/bin/env -S uv run
"""
Example script — rename this file and edit freely.

Run from the api/ directory:
    uv run scripts/example.py

Or via just:
    just script example

---------------------------------------------------------------------
Need an extra dependency not in pyproject.toml?
Add a PEP 723 inline metadata block below the module docstring:

    # /// script
    # requires-python = ">=3.13"
    # dependencies = [
    #   "httpx",
    # ]
    # ///

WARNING: adding that block runs the script in an isolated environment,
which means project packages (e.g. `from app.config import settings`)
will no longer be importable. Stick to one model or the other.
---------------------------------------------------------------------
"""

from app.config import settings


def main() -> None:
    print(f"App: {settings.app_name} | debug={settings.debug}")


if __name__ == "__main__":
    main()
