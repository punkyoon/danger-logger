# danger-logger

This project is for managing docker container service on remote environment.

You just set `docker-compose.yaml` path and container name list that you want to manage

## How to use

1. Set environment variable for passcode

```bash
# Example
$ export PASS_CODE=test1
```

2. Start server

```bash
$ python3 server/server.py
```

3. Connect to server using client program

```bash
$ python3 client/client.py
```

## License

Just unlicense!
