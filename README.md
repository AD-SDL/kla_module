# kla_module

A [MADSci](https://github.com/AD-SDL/MADSci) node module for controlling a KLA Nanomechanics instrument through its HTTP control server.

## Actions

| Action          | Arguments                                     | Description                                                     |
| --------------- | --------------------------------------------- | --------------------------------------------------------------- |
| `load_protocol` | `protocol_files: list[str]`, `message: str?`  | Load protocol files and move the stage to the sample load position |
| `run_protocol`  | `protocol_files: list[str]`, `message: str?`  | Run a batch of protocol (`.NMPROJ`) files                        |
| `check_status`  | none                                          | Query whether a sample run is in progress                       |

`protocol_files` are paths on the KLA control PC, e.g. `C:\Users\Public\Documents\Nanomechanics\Profiles\Default\Make Indents.NMPROJ`.

## Configuration

Settings come from CLI flags, environment variables (prefixed `NODE_`), or a `.env` file:

| Setting           | Env var                | Default                 |
| ----------------- | ---------------------- | ----------------------- |
| `kla_url`         | `NODE_KLA_URL`         | `http://127.0.0.1:8080` |
| `request_timeout` | `NODE_REQUEST_TIMEOUT` | `30.0`                  |
| `node_name`       | `NODE_NAME`            | `kla_node`              |
| `node_url`        | `NODE_URL`             | `http://127.0.0.1:2000` |

## Running

With Docker:

```bash
cp example.env .env   # then edit KLA_URL / NODE_URL
docker compose up --build
```

Locally:

```bash
pdm install -G:all
python src/kla_rest_node.py --kla_url http://<kla-pc>:8080 --node_url http://0.0.0.0:3015
```

## Development

```bash
just init     # install deps and pre-commit hooks
just test     # run unit tests (no hardware needed)
just checks   # run pre-commit
```
