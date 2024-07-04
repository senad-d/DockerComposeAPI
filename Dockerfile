ARG PYTHON_VERSION=3.9-alpine3.19
FROM --platform=linux/amd64 python:${PYTHON_VERSION} as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV MY_JWT_SECRET_KEY=your_jwt_secret_key
ENV API_USERNAME=admin
ENV API_PASSWORD=password

WORKDIR /app

COPY ./conf/dependencies.txt ./conf/nginx.conf /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=conf/requirements.txt,target=requirements.txt \
    python3 -m pip install -r /app/requirements.txt

RUN apk update && \
    xargs -a dependencies.txt apk add --no-cache && \
    rm -rf /var/cache/apk/*

RUN rm /app/dependencies.txt && \
    curl -SL https://github.com/docker/compose/releases/download/v2.28.1/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose &&\
    chmod +x /usr/local/bin/docker-compose
    
COPY ./src /app

RUN mkdir -p /app/source/ && \
    mv /app/nginx.conf /etc/nginx/nginx.conf && \
    rc-update add nginx default

RUN chmod +x /app/gunicorn.sh

EXPOSE 80

CMD ["sh", "-c", "/app/gunicorn.sh"]
