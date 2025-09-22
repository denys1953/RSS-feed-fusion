## Feed Fusion

A small FastAPI app that aggregates RSS feeds. It uses PostgreSQL for storage and Celery (with Redis) for background/scheduled jobs. Run everything with Docker Compose.

### What’s inside
- FastAPI with OpenAPI docs (`/docs`, `/redoc`)
- SQLAlchemy (async/sync), Alembic migrations
- Celery worker and beat, Redis broker/backend

### Quick start (Docker)
1) Create a `.env` in the project root (see example below).
2) Start services:
```bash
docker compose up --build
```
3) Open Swagger: `http://localhost:8000/docs`

### .env example
```env
POSTGRES_DB=feed_fusion
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
SECRET_KEY=change_me
ALGORITHM=HS256
DEBUG=true
# If running outside Docker:
# DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5434/feed_fusion
REDIS_HOST=redis
REDIS_PORT=6379
```

### Local run (optional)
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
celery -A app.celery_worker.celery_app worker --loglevel=info
celery -A app.celery_worker.celery_app beat   --loglevel=info
```

### Migrations
```bash
docker compose exec -it fastapi alembic upgrade head | cat
```

### Notes
- Inside Docker, use `postgres` and `redis` hostnames.
- Postgres is exposed on `localhost:5434` (mapped to container `5432`).



