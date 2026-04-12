# Run both api and client dev servers concurrently.
# Ctrl+C kills both.
dev:
    #!/usr/bin/env bash
    set -e
    trap 'kill 0' SIGINT SIGTERM EXIT
    just api/dev & just client/dev & wait

# Build the client for production
build:
    just client/build

# Run api and client production servers concurrently.
# Ctrl+C kills both.
start:
    #!/usr/bin/env bash
    set -e
    trap 'kill 0' SIGINT SIGTERM EXIT
    just api/start & just client/start & wait
