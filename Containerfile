FROM python:3-alpine AS build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Add whatever packages are needed for building here
RUN apk add --no-cache git

COPY requirements.txt .

RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Assemble the final image
FROM python:3-alpine

ENV PYTHONUNBUFFERED=1

# Set it as an environment variable inside the image
ARG COMMIT_SHA
ENV GIT_COMMIT_SHA=$COMMIT_SHA

WORKDIR /app

COPY --from=build /install /usr/local
COPY src/ /app

ENTRYPOINT [ "python", "main.py" ]