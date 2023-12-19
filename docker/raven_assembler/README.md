## Steps for Building Docker Images

Directly below are instructions for building an image using the provided Dockerfile:

```bash
# See listing of images on computer
docker image ls

# Build from Dockerfile
docker build --no-cache -f Dockerfile --tag=raven_assembly:v0.1.0 .

# Testing, take a peek inside
docker run -ti raven_assembly:v0.1.0 /bin/bash

# Updating Tag  before pushing to DockerHub
docker tag raven_assembly:v0.1.0 asyakhleborodova/raven_assembly:v0.1.0
docker tag raven_assembly:v0.1.0 asyakhleborodova/raven_assembly         # latest

# Check out new tag(s)
docker image ls

# Push new tagged image to DockerHub
docker push asyakhleborodova/raven_assembly:v0.1.0
docker push asyakhleborodova/raven_assembly:latest
```

### Other Recommended Steps

Scan your image for known vulnerabilities:

```bash
docker scan raven_assembly:v0.1.0
```

> **Please Note**: Any references to `asyakhleborodova` should be replaced your username if you would also like to push the image to a non-org account.
