# Kwaai AI Lab - PAI

This section outlines the services defined in the Docker Compose file for this project, including their respective environment variables. These services work together to support the application's functionality, ensuring a seamless operation.

## App Service

The `app` service serves as the main application container, running the Django application.

- **Environment Variables:**
  - `DB_HOST`: Hostname for the database service (`db`).
  - `DB_NAME`: Name of the database used by the application (`devdb`).
  - `DB_USER`: Username for database access (`devuser`).
  - `DB_PASS`: Password for database access (`changeme`).
  - `DEBUG`: Django debug mode (`1` for true).
  - `IMAP_HOST`: IMAP server address (`imap.gmail.com`).
  - `IMAP_EMAIL`: Email address for IMAP login.
  - `IMAP_PASSWORD`: Password for IMAP email account.

- **Ports:**
  - Maps port `8000` on the host to port `8000` on the container, allowing access to the Django development server.

- **Volumes:**
  - Binds the local `./app` directory to `/app` inside the container for live code updates.
  - Uses `dev-static-data` volume for static assets.

## DB Service

The `db` service runs a PostgreSQL database.

- **Environment Variables:**
  - `POSTGRES_DB`: Database name (`devdb`).
  - `POSTGRES_USER`: Username for database access (`devuser`).
  - `POSTGRES_PASSWORD`: Password for database access (`changeme`).

- **Volumes:**
  - Uses `dev-db-data` volume to persist database data.

## Redis Service

The `redis` service provides a Redis server, used for caching and as a message broker for Celery.

- **Ports:**
  - Maps port `6379` on the host to port `6379` on the container, the default Redis port.

## Celery Service

The `celery` service runs the Celery worker.

- **Depends On:**
  - Depends on the `redis` service for message brokering.

- **Command:**
  - Runs Celery with the application's instance, specifying the log level as `info`.

## Celery Beat Service

The `celery_beat` service handles scheduled tasks using Celery Beat.

- **Environment Variables:**
  - `CELERYBEAT_CHDIR`: Specifies the working directory for Celery Beat (`/app/job`).

- **Volumes:**
  - Binds the local `./app` directory to `/app` inside the container for access to the application code.

- **Depends On:**
  - Depends on the `redis` and `celery` services.

## Volumes

- `dev-db-data`: Used by the `db` service to persist database data.
- `dev-static-data`: Used by the `app` service for static assets.
