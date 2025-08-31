## ALX Backend Caching: Property Listings

A Django application demonstrating robust server-side caching with Redis, automatic cache invalidation via Django signals, and a Dockerized setup with PostgreSQL and Redis.

### Features
- **Property listings API**: `GET /properties/` returns all properties as JSON.
- **Per-view caching**: `properties.views.property_list` is cached for 15 minutes using `@cache_page`.
- **Data caching**: `properties.utils.get_all_properties` caches the queryset under the `all_properties` key for an hour by default (`CACHE_DURATION`).
- **Signal-driven invalidation**: `post_save`/`post_delete` signals on `Property` clear the `all_properties` cache key to keep data fresh.
- **Cache metrics helper**: `properties.utils.get_redis_cache_metrics()` reads Redis keyspace hits/misses to gauge cache efficiency.
- **Dockerized stack**: App, PostgreSQL, and Redis services via `docker-compose`.

### Tech Stack
- Django, PostgreSQL, Redis (via `django-redis`), Gunicorn
- Docker, docker-compose

### Endpoints
- **GET** `http://localhost:8000/properties/` — cached JSON list of properties

### Quick Start (Local)
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` at project root (loaded in `settings.py`):
   ```env
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=alxbackendcachingpropertylistings
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   REDIS_LOCATION=redis://localhost:6379
   CACHE_DURATION=3600
   ```
4. Ensure PostgreSQL and Redis are running locally.
5. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Quick Start (Docker)
1. Ensure Docker is installed and running.
2. Create a `.env` file with the same variables as above.
3. Build and start services:
   ```bash
   docker-compose up --build
   ```
4. App runs on `http://localhost:8000` and exposes `GET /properties/`.

### Caching Configuration
- `settings.py` configures Django cache:
  - `CACHES['default']` uses `django_redis.cache.RedisCache` and `REDIS_LOCATION`.
- View cache:
  - `@cache_page(60 * 15)` wraps `property_list`.
- Data cache in `properties/utils.py`:
  - `cache.get('all_properties')` and `cache.set(..., timeout=CACHE_DURATION)`.

### Signals & Invalidation
- `properties/signals.py` listens to `post_save` and `post_delete` for `Property`.
- On changes, it deletes the `all_properties` key to prevent stale reads.
- Signals are hooked in `properties/apps.py` via `PropertiesConfig.ready()`.

### Cache Metrics
- Call `properties.utils.get_redis_cache_metrics()` from admin shell or views to log:
  - Keyspace hits, misses, and hit ratio.

### Development Notes
- Default Django `SECRET_KEY` in settings is for dev only. Set a secure key in production.
- Adjust `ALLOWED_HOSTS` and `DEBUG` appropriately for production.
- Gunicorn is configured in the Dockerfile for production containers.

### Running Tests
Add tests under `properties/tests.py` and run:
```bash
python manage.py test
```

### License
MIT or project-specific (update as needed).


