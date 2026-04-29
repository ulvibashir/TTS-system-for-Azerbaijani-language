FROM python:3.11-slim

# Install espeak-ng
RUN apt-get update && \
    apt-get install -y --no-install-recommends espeak-ng espeak-ng-data && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pipeline code — modules use Path(__file__).parent.parent / "Rules"
# so code must be one level deep: /app/code/*.py → parent.parent = /app/
COPY code/ ./code/

# Rules directory — capital R matches what the Python modules expect on Linux
COPY Rules/ ./Rules/

# Flask API
COPY api/api_server.py .
COPY api/requirements-api.txt .

RUN pip install --no-cache-dir -r requirements-api.txt

EXPOSE 10000

CMD ["python", "api_server.py"]
