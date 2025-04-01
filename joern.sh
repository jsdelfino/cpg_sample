podman run --privileged --rm -it -v $(pwd)/app:/app -v $(pwd)/graph:/graph:rw ghcr.io/joernio/joern:nightly joern-parse -o /graph/joern/cpg.bin /app
podman run --privileged --rm -it -v $(pwd)/app:/app -v $(pwd)/graph:/graph:rw ghcr.io/joernio/joern:nightly joern-export --repr all --format graphml --out /graph/joern/export /graph/joern/cpg.bin

