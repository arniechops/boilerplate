# Boilerplate

An opinionated full-stack boilerplate. Low-level details live in each sub-directory's `CLAUDE.md`.

## Stack

| Layer | Technology |
|---|---|
| **API** | Python 3.13, FastAPI, uv, onion architecture |
| **Client** | Next.js (App Router), Tailwind CSS v4, shadcn/ui, Zustand, TanStack Query, Axios |
| **Task runner** | just (root orchestrates both; each dir has its own justfile) |
| **MCP servers** | Notion, Linear, Parallel (HTTP/OAuth — per-user auth, no keys in the repo) |

## Setup

### 1. Install dependencies

```bash
# API
cd api && uv sync

# Client
cd client && npm install
```

### 2. Configure environment variables

```bash
# API — copy and fill in values
cp api/.env.example api/.env

# Client — copy and fill in values
cp client/.env.local.example client/.env.local
```

### 3. Install Claude Code plugins

```
/plugin
```

Select `frontend-design` and `chrome-devtools-mcp`. Then reload:

```
/reload-plugins
```

### 4. Authenticate MCP servers

MCP server endpoints are pre-configured in `.mcp.json`. Each contributor authenticates with their own account — nothing is stored in the repo.

In your Claude Code session, run:
```
/mcp
```
Follow the OAuth prompts for each server. Tokens are saved to your local Claude config.

### 5. Start the dev servers

```bash
# From the repo root — starts both api and client, Ctrl+C kills both
just dev
```

Or start them individually:
```bash
just api/dev
just client/dev
```

## MCP servers

Configured in `.mcp.json`. All use HTTP/OAuth — no API keys committed to the repo.

| Server | Purpose | Endpoint |
|---|---|---|
| **Notion** | Read/write Notion pages and databases | `https://mcp.notion.com/mcp` |
| **Linear** | Query and manage Linear issues | `https://mcp.linear.app/mcp` |
| **Parallel** | Web search | `https://search-mcp.parallel.ai/mcp` |

## Claude Code plugins

Install via `/plugin` in your Claude Code session.

| Plugin | Purpose |
|---|---|
| **frontend-design** | Generates production-grade UI with high design quality |
| **chrome-devtools-mcp** | Browser automation, debugging, performance, and a11y auditing via Chrome DevTools |

## Project structure

```
/
├── api/          # FastAPI backend — see api/CLAUDE.md
├── client/       # Next.js frontend — see client/CLAUDE.md
├── .mcp.json     # MCP server endpoints (shared; auth is per-user)
└── justfile      # Root task runner
```
