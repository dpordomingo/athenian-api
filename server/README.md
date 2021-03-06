# OpenAPI generated server

## Overview
This server was generated by the [OpenAPI Generator](https://openapi-generator.tech) project. By using the
[OpenAPI-Spec](https://openapis.org) from a remote server, the server stub was generated driven by
the [Connexion](https://github.com/zalando/connexion) library on top of aiohttp.

## Requirements
Python 3.5.2+

## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m athenian.api --state-db sqlite:// --metadata-db sqlite:// --ui
```

You may replace `sqlite://` (in-memory zero-configuration sample DB stub) with a real
[SQLAlchemy connection string](https://docs.sqlalchemy.org/en/13/core/engines.html).

and open your browser to here:

```
http://localhost:8080/v1/ui/
```

Your OpenAPI definition lives here:

```
http://localhost:8080/v1/openapi.json
```

To launch the integration tests, use pytest:
```
sudo pip install -r test-requirements.txt
pytest
```

## Operations

[Deployment.](DEPLOYMENT.md)

[DB migration.](server/athenian/api/models/state/README.md)

Prometheus monitoring: `http://localhost:8080/status`.

Generating admin invitations:

```
ATHENIAN_INVITATION_KEY=secret python3 -m athenian.api.invite_admin sqlite://
```

Replace `sqlite://` with the actual DB endpoint and `secret` with the actual passphrase.

Running with real Cloud SQL databases:

```
cloud_sql_proxy -instances=athenian-1:us-east1:owl-cloud-sql-2f803bb6=tcp:5432

--metadata-db=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/metadata
--state-db=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/state
```

## Development

Install the linters:

```
pip install -r lint-requirements.txt
```

Validate your changes:

```
cd server
flake8
pytest -s
```

Generate sample SQLite metadata and state databases:

```
docker run --rm -e DB_DIR=/io -v$(pwd):/io --entrypoint python3 athenian/api /server/tests/gen_sqlite_db.py
``` 

You should have two SQLite files in `$(pwd)`: `mdb.sqlite` and `sdb.sqlite`.

Obtain Auth0 credentials for running locally: [webapp docs](https://github.com/athenianco/athenian-webapp/blob/master/docs/CONTRIBUTING.md#auth0-and-github-app-local-testing).

### Running tests against a real metadata DB

```
export AUTH0_DOMAIN=...
export AUTH0_AUDIENCE=...
export AUTH0_CLIENT_ID=...
export AUTH0_CLIENT_SECRET=...
export OVERRIDE_MDB=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/db_name
cd server
pytest -s
```

## Running the API server locally

Alternatively, you can locally build and run the docker image:

```
# Build the API image
make docker-build

# Run the API container
make run-api
```

And open http://localhost:8080/v1/ui

If you want to run your own API image, use instead:
```
# Run the API container
IMAGE=your_api_image:tag make run-api
```

You can erase the API data fixtures created by `make run-api` with:
```
make clean
```

## @gkwillie

The following creates the default user in the state DB:

```
make gkwillie
```

or

```
python3 -m athenian.api.create_default_user postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/state
```

You need to set `ATHENIAN_DEFAULT_USER` to the Auth0 ID of the default user. @gkwillie's `github|60340680`.

## Gods

Let's suppose there is a super admin `adim@athenian.co` and a regular user `marvin@athenian.co`.

1. `vadim@athenian.co` logs in as usual.
2. Call `/v1/become?id=auth0|whatever-belongs-to-marvin@athenian.co`
3. A new record in the DB appears that maps `vadim@athenian.co` (`God.user_id`) to `marvin@athenian.co` (`God.mapped_id`).
4. Any subsequent request from `vadim@athenian.co` is first handled as normal, so Auth0 checks whether the user is `vadim@athenian.co`.
5. However, in the end, we check whether `vadim@athenian.co` is a god. If he is, we look up the mapped ID in the DB.
6. We query the mgmt Auth0 API to fetch the full profile of the mapped user - `marvin@athenian.co`.
7. We overwrite the user field of request and additionally set the extra attribute god_id to indicate that the user is a mapped god.
8. API handlers think that the user is `marvin@athenian.co`.
9. But `/v1/become` checks user.god_id and if it exists, it is used in the DB god check instead
of the regular user.id. Thus we don't lose the ability to turn into any other user, including
the empty string (None, the initial default unmapped state).

## Configure Sentry

You can set `SENTRY_PROJECT` and `SENTRY_KEY` environment variables to automatically send the local server crashes to Sentry.

If you're running the API with docker (using `make run-api` from above), you should stop the server, add the Sentry values into the `.env` file that will be in the root folder of `athenian-api`, and start the server again (with `make run-api`).

`SENTRY_ENV` sets the [environment](https://docs.sentry.io/enriching-error-data/environments/?platform=python).
That should be touched only for the real deployments.

Optionally, specify `ATHENIAN_DEV_ID` to identify yourself in Sentry reports.

## Prevent file overriding

After the first generation, add edited files to _.openapi-generator-ignore_ to prevent generator to overwrite them. Typically:
```
server/controllers/*
test/*
*.txt
```
