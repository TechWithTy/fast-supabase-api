# Fast Supabase API Backend

## Overview

This repository is a backend-only template designed for scalable, production-grade applications. It features:

- **PostgreSQL** as the primary database
- **Supabase** integration for authentication and real-time features
- **Redis** for caching and background task queues
- **Stripe** for payments and billing (via built-in submodule)
- **MCP (Model Context Protocol)** integration for modular AI workflows
- **Docker Compose** for local development and deployment orchestration

> **Note:** This project is backend only. For full-stack or frontend integration, see the corresponding frontend repository or create your own client.

---

## 🐳 Docker Compose Features

This project’s `docker-compose.yml` orchestrates a full suite of production-ready backend services:

- **PostgreSQL (`db`)**: Main relational database with healthchecks and persistent storage.
- **Redis (`redis`)**: Fast in-memory cache, background task broker, and pub/sub support.
- **Adminer (`adminer`)**: Web-based database admin UI for PostgreSQL.
- **cAdvisor (`cadvisor`)**: Real-time container resource monitoring.
- **Celery (`celery`, `celery-beat`)**: Distributed task queue and scheduler, fully integrated with Redis and Postgres.
- **Prometheus (`prometheus`)**: Metrics and monitoring for all services.
- **Grafana (`grafana`)**: Beautiful dashboards and alerting for metrics visualization.
- **Stripe Integration (`stripe_home` submodule)**: Built-in payment and billing workflows.
- **Supabase Integration (`supabase_home` submodule)**: Auth, storage, and real-time features.
- **MCP Server (`mcp-server`)**: Modular AI/LLM workflows and context protocol integration.
- **Traefik (labels)**: Reverse proxy and automatic HTTPS support (if enabled).
- **Prestart/Backend**: Automated scripts for migrations, environment setup, and main API service.
- **Apache Pulsar (optional)**: Advanced event streaming and pub/sub (if enabled in your stack).

> All services are networked for secure, scalable microservice communication.

---

## ⚙️ CI/CD Pipeline

- **GitHub Actions**: Out-of-the-box workflows for linting, testing, and building Docker images.
- **Automated Testing**: Runs your Python (and JS if present) tests on every pull request and push.
- **Docker Build & Push**: Optionally build and publish Docker images to your container registry on release.
- **Deployment Ready**: Easily extend CI/CD to deploy to AWS, GCP, Azure, or DigitalOcean with minimal config.
- **.env Management**: Use secrets for safe environment variable injection in CI/CD.

---

## 📝 Example: Starting All Services

```bash
docker-compose up --build
```

- All backend, database, cache, monitoring, and AI/payment integrations will start automatically.
- Access Grafana dashboards, Adminer DB UI, and Prometheus metrics in your browser (see `docker-compose.yml` for ports).

---

## 📈 Scaling, Monitoring, and Observability

- Add more Celery workers for background task scaling.
- Monitor resource usage and performance in real time with Prometheus + Grafana.
- Extend with additional services (e.g., extra databases, message brokers) as your project grows.

---

## 🔒 Security & Best Practices

- All secrets are managed via `.env` files (never commit real secrets).
- Healthchecks and restart policies ensure high availability.
- Use Traefik and HTTPS for secure public deployments.

---

## 🚀 Cloning with Submodules

This project uses several git submodules for reusable backend components.  
**To ensure your clone includes all required code, always use the `--recursive` flag!**

```bash
git clone --recursive https://github.com/TechWithTy/fast-supabase-api.git
```

If you already cloned the repo **without** `--recursive`, initialize and update submodules with:

```bash
git submodule update --init --recursive
```

---

## 🛠️ Backend Quickstart

1. **Copy and configure your environment variables:**
   - Choose the appropriate `.env.example` for your environment (local, prod, etc.) and copy it to `.env`.
   - Fill in all required secrets and configuration values for Postgres, Supabase, Redis, Stripe, and MCP.

2. **Install dependencies and run:**
   - Using Docker Compose (recommended):
     ```bash
     docker-compose up --build
     ```
   - All services (API, DB, Redis, Stripe, MCP, etc.) will start automatically.

---

## 🧩 Built-in Integrations

- **Supabase**: Auth, real-time, and storage via submodule (`backend/app/supabase_home`)
- **PostgreSQL**: Main relational database (service: `db`)
- **Redis**: Caching, Celery broker, async tasks (service: `redis`)
- **Stripe**: Subscription/payments integration via submodule (`backend/app/stripe_home`)
- **MCP (Model Context Protocol)**: Modular AI/LLM workflows (service: `mcp-server`, submodule: `backend/app/model_context_protocol`)

---

## 🏗️ Scaling & Extending

- **Redis** is ready for scaling background tasks, caching, and pub/sub. When scaling, update `docker-compose.yml` to add more worker services as needed.
- **Supabase** integration supports scalable auth and real-time features out of the box.
- **Stripe** integration is modular—extend or replace payment logic as needed.
- **MCP** enables rapid AI/LLM workflow extension; add new tools/resources in `model_context_protocol`.

---

## 📦 Project Structure

```
fast-supabase-api/
├── backend/
│   └── app/
│       ├── api/            # FastAPI app code
│       ├── *_home/         # Submodules for Supabase, Stripe, MCP, etc.
│       └── ...
├── docker/                 # Dockerfiles for prod/dev
├── .env.example            # Example env files
├── docker-compose.yml      # Multi-service orchestration
└── ...
```

---

## 🛡️ Security & Best Practices

- Never commit secrets or production credentials to the repo.
- Keep your repo private if it contains business logic.
- Use `.env` files for all sensitive configuration.

---

## 📚 References & Credits

- Inspired by [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/) and [The Clean Coder](https://www.oreilly.com/library/view/the-clean-coder/9780132542913/).
- Built by Ty the Programmer.

---

For more, see the original README and docs inside each submodule or integration folder.
