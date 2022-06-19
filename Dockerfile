# Build a virtualenv using the appropriate Debian release
# * Install python3-venv for the built-in Python3 venv module (not installed by default)
# * Install gcc libpython3-dev to compile C Python modules
# * Update pip to support bdist_wheel
FROM docker.io/debian:bullseye-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev wget && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip

# pip install and download corpora
FROM build AS install
COPY app/requirements.txt app/requirements.txt
RUN /venv/bin/pip install --disable-pip-version-check -r app/requirements.txt && \
    /venv/bin/python -m nltk.downloader -d /venv/nltk_data wordnet omw-1.4

# Copy the the necessary files into the distroless image
FROM gcr.io/distroless/python3-debian11 AS pre
COPY ./app /
COPY --from=install /venv /venv

# Basically squashing the COPY commands in the final image
FROM gcr.io/distroless/python3-debian11
COPY --from=pre / /
ENTRYPOINT ["/venv/bin/python", "bot.py"]
