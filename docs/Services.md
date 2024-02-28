# Docker Compose Documentation

This document provides detailed information about the `docker-compose.yml` file used to set up and run the various services required for the project. The Docker Compose configuration specifies multiple services, volumes, and environment variables crucial for the application's operation.

## Services

### `app`

- **Description**: The main application service that runs the Django server.
- **Build Arguments**:
  - `DEV`: Indicates whether the application is running in a development environment.
- **Ports**:
  - Maps port 8000 of the container to port 8000 on the host, allowing access to the Django application.
- **Volumes**:
  - Binds the local `./app` directory to `/app` in the container for application code.
  - Uses `dev-static-data` volume for static data.
- **Commands**: Executes Django management commands to wait for the database, apply migrations, and start the development server.
- **Environment Variables**: Configures database connection, debugging, IMAP settings for downloading user data, and API keys for external services.
- **Dependencies**: Depends on the `db`, `redis`, `celery`, and `celery_beat` services.

### `db`

- **Image**: Uses `postgres:13-alpine` as the base image.
- **Volumes**:
  - Persists PostgreSQL data using `dev-db-data` volume.
- **Environment Variables**: Configures the PostgreSQL database, user, and password.

### `redis`

- **Image**: Uses the latest Redis image.
- **Ports**:
  - Exposes Redis on port 6379 of both the container and host.
- **Command**: Starts the Redis server with a bind to `0.0.0.0`.

### `celery`

- **Description**: Runs Celery workers for background tasks.
- **Dependencies**: Depends on the `redis` service for message brokering.
- **Command**: Starts Celery workers with logging.

### `celery_beat`

- **Description**: Runs the Celery Beat service for scheduled tasks.
- **Command**: Starts Celery Beat with logging.
- **Volumes**:
  - Shares the `./app` directory with the container.
- **Dependencies**: Depends on the `redis` and `celery` services.
- **Environment Variables**: Configures the working directory for Celery Beat.

## Volumes

- `dev-db-data`: Persists database data.
- `dev-static-data`: Stores static files for the application.
- `celerybeat-data`: (Mentioned but not used in the provided configuration. Could be intended for persisting Celery Beat schedules.)

## Environment Variables

The following environment variables need to be specified either in a `.env` file or in the environment where `docker-compose` is run:

- Database-related: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
- Debugging: `DEBUG`
- IMAP for downloading user data: `IMAP_HOST`, `IMAP_EMAIL`, `IMAP_PASSWORD`
- API keys for external services: `OPENAI_API_KEY`, `HUGGINGFACE_ACCESS_TOKEN`
- Celery Beat: `CELERYBEAT_CHDIR`

## Running the Project

To run the project, ensure you have Docker and Docker Compose installed. Place your `.env` file in the project root or export the necessary environment variables