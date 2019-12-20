# How to deploy Athenian API

### Docker image

```
docker build -t athenian/api .
```

### Initialization

```
docker run -it --rm --entrypoint python3 athenian/api -m athenian.api.models.state postgres://user:password@host:port/database
```

### Environment

The server requires:

- (optional) `SENTRY_KEY` and `SENTRY_PROJECT` environment variables to enable error logging.
- (optional) `AUTH0_DOMAIN` and `AUTH0_AUDIENCE` environment variables to enable authorization.
- Accessible PostgreSQL endpoint with the metadata.
- Accessible PostgreSQL endpoint with the server state.
- Exposing the configured HTTP port outside.

### Configuration

Please follow the CLI help:

```
docker run -it --rm athenian/api --help
```

No configuration files are required.

### State

The server's state such as user settings, etc., is stored in a SQL database specified with `--state-db`.