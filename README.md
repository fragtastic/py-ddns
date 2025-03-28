# py-ddns

Dynamically update DNS for various providers.

[![Build and Push Docker Image](https://github.com/fragtastic/py-ddns/actions/workflows/docker-build.yaml/badge.svg)](https://github.com/fragtastic/py-ddns/actions/workflows/docker-build.yaml)

## Providers

Completed:
- Cloudflare

Planned:
- Namecheap

## Installation

Copy `example.env` to `.env`, set the variables directly in `docker-compose.yml`, or configure them using whatever orchestration tool you're using.

A provider must be selected with `DDNS_PROVIDER` and set the appropriate provider specific environment variables must be set.

- `UPDATE_INTERVAL_MINUTES` defaults to `10`.
- `TTL` defaults to `120`

```bash
docker pull ghcr.io/fragtastic/py-ddns:latest
docker run --rm --env-file=.env ghcr.io/fragtastic/py-ddns:latest
```

## Output

```log
[2025-03-28 00:48:51] INFO [Main]: Running git commit: 92oa8wbvacaz0cex7sdqixo64uzgtubop1sy5l60
[2025-03-28 00:48:52] INFO [Main]: Running DDNS check every 5 minute(s)
[2025-03-28 00:48:53] INFO [Cloudflare]: Updated ext.example.com → 123.123.123.123
[2025-03-28 00:48:53] INFO [Main]: IP updated: 123.123.123.123
```
