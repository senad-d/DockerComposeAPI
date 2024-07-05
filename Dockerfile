ARG PYTHON_VERSION=3.12.4-alpine3.20

FROM alpine:3.20 as downloader

RUN apk add --no-cache curl && \
    curl -SL https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

FROM --platform=linux/amd64 python:${PYTHON_VERSION} as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV MY_JWT_SECRET_KEY=your_jwt_secret_key
ENV API_USERNAME=admin
ENV API_PASSWORD=password

WORKDIR /app

COPY ./conf/dependencies.txt ./conf/nginx.conf /app
COPY --from=downloader /usr/local/bin/docker-compose /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=conf/requirements.txt,target=requirements.txt \
    python3 -m pip install -r /app/requirements.txt

RUN apk update && \
    xargs -a dependencies.txt apk add --no-cache && \
    rm -rf /var/cache/apk/*

RUN rm /app/dependencies.txt

COPY ./src /app

RUN mkdir -p /app/source/ && \
    mv /app/nginx.conf /etc/nginx/nginx.conf && \
    rc-update add nginx default

RUN chmod +x /app/gunicorn.sh

EXPOSE 80

CMD ["sh", "-c", "/app/gunicorn.sh"]
