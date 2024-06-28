# api-demo

## Build container
```shell
docker compose build 
```

## Run container
```shell
docker compose up -d --force-recreate --remove-orphans
```

## Test the API
```shell
curl -X POST -H "Content-Type: application/json" -d '{"command":"docker-compose -f source/docker-compose.yml up -d"}' http://localhost:8080/runcmd
```