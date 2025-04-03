FROM ghcr.io/astral-sh/uv:python3.12-bookworm

WORKDIR /app

COPY [ "pyproject.toml",  "uv.lock", "/app/" ]

COPY zirak.py /app/zirak.py
COPY ./src /app/src
COPY ./entrypoint.sh /entrypoint.sh

CMD '/entrypoint.sh'




