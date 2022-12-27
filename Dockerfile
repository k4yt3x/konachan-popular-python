# Name: KonachanPopular (Python) Dockerfile
# Creator: K4YT3X
# Date Created: December 26, 2022
# Last Modified: December 26, 2022

FROM docker.io/python:3.11.1-alpine3.17

COPY . /build
RUN pip install /build \
    && rm -rf /build

ENTRYPOINT ["/usr/local/bin/python", "-m", "konachan_popular"]
