podman run --privileged --rm -v $(pwd)/app:/app:rw -v $(pwd)/graph:/graph:rw -t ghcr.io/appthreat/atom atom -l python -o /graph/atom/app.atom --export-atom --export-format graphml --export-dir /graph/atom/export /app

