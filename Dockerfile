FROM python:3.11-slim
WORKDIR /project
RUN apt-get update && apt-get install -y --no-install-recommends build-essential git curl libffi-dev && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml .
COPY src src
RUN pip install --no-cache-dir .
COPY scripts scripts
COPY tests tests
CMD ["python", "-m", "unittest", "discover", "-s", "tests", "-v"]
