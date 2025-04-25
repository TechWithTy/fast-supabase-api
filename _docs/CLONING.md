# Fast Supabase API Backend Template

## 🚀 Backend Setup: Cloning with Submodules

This project uses several git submodules for reusable backend components.

**To ensure your clone includes all required code, always use the `--recursive` flag!**

### 1. Clone the Repository with Submodules

```bash
git clone --recursive https://github.com/TechWithTy/fast-supabase-api.git
```

If you already cloned the repo **without** `--recursive`, initialize and update submodules with:

```bash
git submodule update --init --recursive
```

### 2. Keeping Submodules Up to Date

To pull the latest changes for both the main repo and all submodules:

```bash
git pull --recurse-submodules
git submodule update --init --recursive
```

### 3. Troubleshooting

- If you see missing files or folders (especially in `backend/app/*_home`), you likely forgot to initialize submodules.
- Always use the above commands after switching branches if submodules are updated.

---

## 🛠️ Backend Quickstart

1. **Copy and configure your environment variables:**
   - Choose the appropriate `.env.example` for your environment (local, prod, etc.) and copy it to `.env`.
   - Fill in all required secrets and configuration values.

2. **Install dependencies:**
   - Using Docker Compose (recommended):
     ```bash
     docker-compose up --build
     ```
   - Or install Python dependencies manually:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the backend:**
   - With Docker Compose, all services (API, DB, etc.) will start automatically.
   - For manual/local dev, run the main FastAPI app entrypoint (see `backend/app/api/main.py`).

---

## 📦 Project Structure Overview

```
fast-supabase-api/
├── backend/
│   └── app/
│       ├── api/            # FastAPI app code
│       ├── ...
│       └── *_home/         # Submodules for reusable integrations
├── docker/                 # Dockerfiles for prod/dev
├── .env.example            # Example env files
├── docker-compose.yml      # Multi-service orchestration
└── ...
```

---

## 🧩 Using Copier for Project Generation

This repository supports generating a new project using [Copier](https://copier.readthedocs.io).

- Copier will copy all files, ask configuration questions, and update `.env` files with your answers.

### Install Copier

```bash
pip install copier
# or
pipx install copier
```

---

## 📝 Contributing & Customization

- Follow DRY, SOLID, and clean code principles.
- Use type hints, write tests, and document your tools/resources.
- For custom integrations, add new submodules or backend services as needed.

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
