# ── Stage 1: Build Next.js static frontend ───────────────────────────────────
FROM node:20-slim AS frontend

WORKDIR /build

COPY package*.json ./
RUN npm install

COPY next.config.ts tsconfig.json postcss.config.mjs ./
COPY src/ ./src/

RUN npm run build
# Output is in /build/out/


# ── Stage 2: Python Flask server ─────────────────────────────────────────────
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends espeak-ng espeak-ng-data && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Pipeline code — modules use Path(__file__).parent.parent / "Rules"
# so /app/code/*.py → parent.parent = /app/ → looks for /app/Rules/
COPY code/ ./code/
COPY Rules/ ./Rules/

# Flask server
COPY server.py .
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

# Copy built frontend from Stage 1
COPY --from=frontend /build/out ./static/

EXPOSE 10000

CMD ["python", "server.py"]
