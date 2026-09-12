FROM python:3.13-slim

# ffmpeg is the only system dependency the music cog needs.
RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e .

# Per-guild settings live here (storage.py); mount it as a volume so a
# container rebuild/restart never loses configuration.
VOLUME ["/app/data"]

CMD ["overlord"]
