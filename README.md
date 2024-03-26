# Kwaai AI Lab - PAI

## Docker Compose Setup for Django App and PostgreSQL

This Docker Compose configuration is designed for a Django app and PostgreSQL database.

## Services

### 1. app

- **Build**: The Django app is built from the current context (`.`) with the DEV flag set to true.
- **Ports**: The app is exposed on port 8000.
- **Volumes**:
  - `./app` is mounted to `/app` in the container.
  - `dev-static-data` is mounted to `/vol/web` for static data.
- **Command**: Runs Django management commands (`wait_for_db`, `migrate`, and `runserver`) on startup.
- **Environment**:
  - `DB_HOST`: Database host name (`db`).
  - `DB_NAME`: Database name (`devdb`).
  - `DB_USER`: Database user (`devuser`).
  - `DB_PASS`: Database password (`changeme`).
  - `DEBUG`: Enables Django debug mode (`1`).

### 2. db

- **Image**: PostgreSQL 13 Alpine.
- **Volumes**: `dev-db-data` is mounted to `/var/lib/postgresql/data` for persistent data.
- **Environment**:
  - `POSTGRES_DB`: PostgreSQL database name (`devdb`).
  - `POSTGRES_USER`: PostgreSQL database user (`devuser`).
  - `POSTGRES_PASSWORD`: PostgreSQL database password (`changeme`).

#### Django Models Relationships Documentation

## User Model

| Field Name | Type | Description |
|------------|------|-------------|
| id | UUID | Primary key for the user model |
| username | CharField | Unique username for the user |
| is_active | BooleanField | Indicates whether the user account is active |
| is_staff | BooleanField | Indicates whether the user has staff privileges |
| ... | ... | Other fields from AbstractBaseUser and PermissionsMixin |

## ImapCredentials Model

| Field Name | Type | Description |
|------------|------|-------------|
| user | ForeignKey | References the User model |
| email | EmailField | Primary key for the email credentials |
| password | CharField | Password for the email account |
| imap_server | CharField | IMAP server address for the email account |

## ImapEmail Model

| Field Name | Type | Description |
|------------|------|-------------|
| user | ForeignKey | References the User model |
| subject | CharField | Subject of the email |
| from_email | CharField | Sender's email address |
| timestamp | CharField | Timestamp of the email |
| body | TextField | Body content of the email |


## Dependencies

- The `app` service depends on the `db` service.

## IMAP Search Keys

| Key          | Description                                                                                                  |
|--------------|--------------------------------------------------------------------------------------------------------------|
| ALL          | All messages in the mailbox; the default initial key for ANDing.                                            |
| ANSWERED     | Messages with the \Answered flag set.                                                                        |
| BCC          | Messages that contain the specified string in the envelope structure's BCC field.                             |
| BEFORE       | Messages whose internal date is earlier than the specified date.                                             |
| BODY         | Messages that contain the specified string in the body of the message.                                        |
| CC           | Messages that contain the specified string in the envelope structure's CC field.                              |
| DELETED      | Messages with the \Deleted flag set.                                                                         |
| DRAFT        | Messages with the \Draft flag set.                                                                           |
| FLAGGED      | Messages with the \Flagged flag set.                                                                         |
| FROM         | Messages that contain the specified string in the envelope structure's FROM field.                             |
| HEADER       | Messages that have a header with the specified field-name and that contain the specified string in the text of the header. |
| KEYWORD      | Messages with the specified keyword flag set.                                                               |
| LARGER       | Messages with an [RFC-2822] size larger than the specified number of octets.                                  |
| NEW          | Messages that have the \Recent flag set but not the \Seen flag. This is functionally equivalent to "(RECENT UNSEEN)". |
| NOT          | Messages that do not match the specified search key.                                                         |
| OLD          | Messages that do not have the \Recent flag set. This is functionally equivalent to "NOT RECENT" (as opposed to "NOT NEW"). |
| ON           | Messages whose internal date is within the specified date.                                                  |
| OR           | Messages that match either search key.                                                                      |
| RECENT       | Messages that have the \Recent flag set.                                                                    |
| SEEN         | Messages that have the \Seen flag set.                                                                      |
| SENTBEFORE   | Messages whose Date: header is earlier than the specified date.                                              |
| SENTON       | Messages whose Date: header is within the specified date.                                                    |
| SENTSINCE    | Messages whose Date: header is within or later than the specified date.                                       |
| SINCE        | Messages whose internal date is within or later than the specified date.                                     |
| SMALLER      | Messages with an [RFC-2822] size smaller than the specified number of octets.                                 |
| SUBJECT      | Messages that contain the specified string in the envelope structure's SUBJECT field.                         |
| TEXT         | Messages that contain the specified string in the header or body of the message.                              |
| TO           | Messages that contain the specified string in the envelope structure's TO field.                               |
| UID          | Messages with unique identifiers corresponding to the specified unique identifier set. Sequence set ranges are permitted. |
| UNANSWERED   | Messages that do not have the \Answered flag set.                                                            |
| UNDELETED    | Messages that do not have the \Deleted flag set.                                                             |
| UNDRAFT      | Messages that do not have the \Draft flag set.                                                               |
| UNFLAGGED    | Messages that do not have the \Flagged flag set.                                                             |
| UNKEYWORD    | Messages that do not have the specified keyword flag set.                                                    |
| UNSEEN       | Messages that do not have the \Seen flag set.                                                               |

## How to Use

1. Ensure Docker and Docker Compose are installed.
2. Run the following command in the project root directory to build and start the services:

   ```bash
   docker-compose up --build
   ```

3. The Django app will be accessible at `http://localhost:8000`.

4. Swagger API Documentation:
   - Visit `http://localhost:8000/api/docs/` to access Swagger documentation for the API services.

## Notes

- Ensure proper adjustments to environment variables (`DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASS`) for production use.
- Debug mode is enabled in this setup; it's recommended to disable it in a production environment.
- The `depends_on` section ensures that the `app` service starts after the `db` service.

For additional configurations and deployment considerations, refer to the documentation of Django and PostgreSQL.
```
