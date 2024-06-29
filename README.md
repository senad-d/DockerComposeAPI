# api-demo

## Build container
```shell
docker compose build 
```

## Run container
```shell
docker compose up -d --force-recreate --remove-orphans
```

## Access login credentials
```shell
curl -X POST http://localhost:8080/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}'

TOKEN=$(curl -X POST http://localhost:8080/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "password"}' | jq -r .access_token)
```

## Test the API
```shell
curl -X POST http://localhost:8080/runcmd \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d '{"command":"docker-compose -f source/docker-compose.yml up -d"}'
```