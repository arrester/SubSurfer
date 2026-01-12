FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libxml2-dev \
       libxslt1-dev \
       libffi-dev \
       libssl-dev \
       git \
    && rm -rf /var/lib/apt/lists/*

# Install package dependencies using setup.py (uses install_requires to avoid conflicting pins)
COPY setup.py README.md MANIFEST.in /app/
RUN pip install --no-cache-dir .

# Copy project sources (we run as a module; this allows local changes via volume)
COPY . /app

# Default entrypoint runs the CLI as a module; user can pass CLI args to docker run
ENTRYPOINT ["python", "-m", "subsurfer"]
CMD ["--help"]
