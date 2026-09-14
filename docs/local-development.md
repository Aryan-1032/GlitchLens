# Local Development

This document describes the validated local development environment for the AI Web Testing Platform and its Saleor reference application.

## 1. Local workspace

The development workspace is organized as:

```text
F:\open source\
├── saleor-platform\
├── storefront\
└── ai-web-testing-platform\
    ├── core\
    ├── adapters\
    │   ├── saleor\
    │   └── demo_adapter\
    ├── tests\
    ├── vision\
    ├── backend\
    ├── dashboard\
    ├── database\
    ├── artifacts\
    ├── datasets\
    ├── docker\
    └── docs\
```

`ai-web-testing-platform` contains our own platform code.

`saleor-platform` and `storefront` are external reference applications used as the system under test. They should not be mixed into the platform's source code.

## 2. Validated development environment

This setup has been validated on Windows with:

| Component      | Version / Configuration |
| -------------- | ----------------------- |
| Docker Desktop | 4.72.0                  |
| Docker Engine  | 29.4.2                  |
| Docker Compose | v5.1.3                  |
| Docker context | `desktop-linux`         |
| Node.js        | 24.x                    |
| pnpm           | 10.28.1                 |
| Saleor         | 3.23                    |
| PostgreSQL     | 15 Alpine               |
| Cache          | Valkey 8.1 Alpine       |

Docker Desktop must be running before starting Saleor.

## 3. Local services

| Service                       | Address                          |
| ----------------------------- | -------------------------------- |
| Saleor Storefront             | `http://localhost:3000`          |
| Saleor GraphQL API            | `http://localhost:8000/graphql/` |
| Saleor API root               | `http://localhost:8000`          |
| Saleor Dashboard              | `http://localhost:9000`          |
| PostgreSQL                    | `localhost:5432`                 |
| Valkey/Redis-compatible cache | `localhost:6379`                 |
| Mailpit                       | `http://localhost:8025`          |
| Jaeger                        | `http://localhost:16686`         |

## 4. Initial Saleor platform setup

Open PowerShell:

```powershell
cd "F:\open source\saleor-platform"
```

Run database migrations:

```powershell
docker compose run --rm api python3 manage.py migrate
```

Populate the database with development/sample data:

```powershell
docker compose run --rm api python3 manage.py populatedb --createsuperuser
```

For the local development environment, the generated development administrator is:

```text
Email: admin@example.com
Password: admin
```

These credentials are development-only and must never be reused for production environments.

Start Saleor:

```powershell
docker compose up
```

Keep this terminal running while developing or testing against Saleor.

## 5. Verify Saleor containers

In another PowerShell window:

```powershell
cd "F:\open source\saleor-platform"
docker compose ps
```

The following services should be running:

```text
api
cache
dashboard
db
jaeger
mailpit
worker
```

The API should be available at:

```text
http://localhost:8000
```

The Dashboard should be available at:

```text
http://localhost:9000
```

## 6. Saleor storefront setup

The storefront repository is located at:

```text
F:\open source\storefront
```

Its dependencies are installed using pnpm:

```powershell
cd "F:\open source\storefront"
pnpm install
```

The local environment configuration is stored in:

```text
.env
```

At minimum, it contains configuration equivalent to:

```env
NEXT_PUBLIC_SALEOR_API_URL=http://localhost:8000/graphql/
NEXT_PUBLIC_DEFAULT_CHANNEL=<SALEOR_CHANNEL_SLUG>
NEXT_PUBLIC_STOREFRONT_URL=http://localhost:3000/
```

The actual Saleor channel slug should be obtained from:

```text
Saleor Dashboard → Configuration → Channels
```

The `.env` file must never be committed.

Its Git ignore behavior has been verified using:

```powershell
git check-ignore -v .env
```

Expected behavior:

```text
.gitignore:7:.env    .env
```

## 7. Start the storefront

Run:

```powershell
cd "F:\open source\storefront"
pnpm dev
```

Open:

```text
http://localhost:3000
```

## 8. Local smoke test

A successful environment must pass the following basic test:

1. Open the storefront at `http://localhost:3000`.
2. Confirm products from the seeded Saleor catalog are displayed.
3. Open a product detail page.
4. Add a product to the cart.
5. Open the Saleor Dashboard at `http://localhost:9000`.
6. Log in successfully using the local administrator.
7. Confirm the GraphQL/API is reachable at `http://localhost:8000/graphql/`.

If all checks pass, the local Saleor target environment is suitable for automated testing.

## 9. Normal development startup

After initial setup, migrations and `populatedb` normally do not need to be rerun.

Start the Saleor backend:

```powershell
cd "F:\open source\saleor-platform"
docker compose up
```

In another terminal, start the storefront:

```powershell
cd "F:\open source\storefront"
pnpm dev
```

The AI Web Testing Platform will eventually execute tests against these services.

## 10. Stop the environment

Stop the storefront using:

```text
Ctrl+C
```

Stop Saleor using:

```text
Ctrl+C
```

or from the Saleor platform directory:

```powershell
docker compose down
```

Using `docker compose down` does not normally remove named database volumes.

Do not use destructive volume-removal commands unless resetting the environment intentionally.

## 11. Restart verification

Before P00 is considered complete, perform one restart test.

Stop the Saleor stack:

```powershell
docker compose down
```

Start it again:

```powershell
docker compose up
```

Then restart the storefront:

```powershell
pnpm dev
```

Verify that:

```text
Storefront → http://localhost:3000
API        → http://localhost:8000
Dashboard  → http://localhost:9000
```

still work and that previously seeded catalog data remains available.

## 12. Security rules

Never commit:

```text
.env
API keys
access tokens
cookies
database passwords
Gemini API keys
production credentials
private datasets
```

Where configuration examples are required, commit `.env.example` files containing placeholders rather than real secrets.

## 13. P00 completion criteria

P00 — Set up Saleor local environment is complete when the Saleor API, Dashboard, and Storefront run locally; sample catalog data is available; the storefront can browse products and add products to the cart; environment files are excluded from Git; startup instructions are documented; and the environment survives a clean restart without losing the seeded data.
