# 🗳️ Ultimate Voting Machine — Multi-Container Dockerized Application

<div align="center">

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docs.docker.com/compose/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16--Alpine-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/Nginx-Alpine-009639?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

[![GitHub Stars](https://img.shields.io/github/stars/Jani-shiv/Voting-Docker-image?style=for-the-badge&logo=github&color=f59e0b)](https://github.com/Jani-shiv/Voting-Docker-image/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Jani-shiv/Voting-Docker-image?style=for-the-badge&logo=github&color=3b82f6)](https://github.com/Jani-shiv/Voting-Docker-image/network/members)
[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Follow%20%40shiv--jani-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shiv-jani/)

</div>

---

An interactive, responsive voting application featuring a high-contrast brutalist Bento-grid UI. The project supports both **standalone local execution** (Flask + SQLite) and a **production-ready 3-tier microservice architecture** containerized with **Docker** and orchestrated using **Docker Compose** (Nginx + Flask + PostgreSQL).

---

## 📑 Table of Contents
- [Architecture Overview](#-architecture-overview)
- [Docker Hub Published Images](#-docker-hub-published-images)
- [Quick Start with Docker Compose](#-quick-start-with-docker-compose-recommended)
- [Architecture Deep Dive](#-architecture-deep-dive)
- [API Reference](#-api-reference)
- [Local Standalone Setup (Without Docker)](#-local-standalone-setup-without-docker)
- [Essential Docker Commands](#-essential-docker-commands)
- [Star History](#-star-history)
- [Project Directory Structure](#-project-directory-structure)
- [Author & Connect](#-author--connect)
- [License](#-license)

---

## 🏛 Architecture Overview

The multi-container production setup decouples presentation, business logic, and persistence into isolated Docker containers connected over a private bridge network:

```
                  ┌─────────────────────────────────────┐
                  │    Client Browser / End User        │
                  └──────────────────┬──────────────────┘
                                     │  HTTP Request (Port 8085)
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      voting_frontend (Nginx)        │
                  │  - Static Asset Delivery (HTML/CSS) │
                  │  - Reverse Proxy for /api/* routes  │
                  └──────────────────┬──────────────────┘
                                     │  Internal Proxy: http://backend:5000
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      voting_backend (Flask)         │
                  │  - REST API & Validation            │
                  │  - Auto Database Connection Retry   │
                  └──────────────────┬──────────────────┘
                                     │  Internal Connection: db:5432
                                     ▼
                  ┌─────────────────────────────────────┐
                  │      voting_db (PostgreSQL 16)      │
                  │  - Persistent SQL Table Storage     │
                  │  - Named Volume: postgres_data      │
                  └─────────────────────────────────────┘
```

### Component Roles

| Service | Container Name | Technology | Internal Port | Exposed Host Port | Purpose |
|---|---|---|---|---|---|
| **Frontend** | `voting_frontend` | Nginx Alpine | 80 | **`8085`** | Serves static assets & reverse-proxies `/api/*` requests to backend |
| **Backend** | `voting_backend` | Python 3.12 / Flask | 5000 | **`5000`** | Processes votes, serves results, and enforces business logic |
| **Database** | `voting_db` | PostgreSQL 16 Alpine | 5432 | **`5432`** | Stores persistent voting records in Docker volume `postgres_data` |

---

## 📦 Docker Hub Published Images

Prebuilt, ready-to-run container images are publicly hosted on Docker Hub:

- **Frontend Image**: [`jani712/voting-frontend:latest`](https://hub.docker.com/r/jani712/voting-frontend)
  ```bash
  docker pull jani712/voting-frontend:latest
  ```
- **Backend Image**: [`jani712/voting-backend:latest`](https://hub.docker.com/r/jani712/voting-backend)
  ```bash
  docker pull jani712/voting-backend:latest
  ```

---

## 🚀 Quick Start with Docker Compose (Recommended)

### 1. Clone the Repository
```bash
git clone https://github.com/Jani-shiv/Voting-Docker-image.git
cd Voting-Docker-image
```

### 2. Build and Launch Containers
```bash
docker compose up --build
```
> To run in background (detached mode):
> ```bash
> docker compose up --build -d
> ```

### 3. Open the Application
Once the containers are running and the database health check passes, open your browser:
👉 **[http://localhost:8085](http://localhost:8085)**

- Enter your voter name.
- Select your candidate card (**Oggy**, **Hathori**, **Doremon**, or **Sinchan**).
- Click **"Cast Your Vote"**.
- View dynamic, live-updating standings!

---

## 🔌 API Reference

The backend exposes clean REST API endpoints accessible through Nginx at `http://localhost:8085/api/` or directly on port `5000`:

### 1. Health Check
- **Endpoint**: `GET /api/health`
- **Response**:
  ```json
  {
    "service": "backend",
    "status": "healthy"
  }
  ```

### 2. Submit a Vote
- **Endpoint**: `POST /api/vote`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "name": "Alex",
    "party": "Oggy"
  }
  ```
- **Success Response (200 OK)**:
  ```json
  {
    "message": "Vote cast successfully!",
    "success": true
  }
  ```
- **Validation Error (400 Bad Request)**:
  ```json
  {
    "error": "Name and party are required"
  }
  ```

### 3. Fetch Standings
- **Endpoint**: `GET /api/results`
- **Response**:
  ```json
  {
    "Doremon": 12,
    "Hathori": 8,
    "Oggy": 15,
    "Sinchan": 10
  }
  ```

---

## 💻 Local Standalone Setup (Without Docker)

You can also run the self-contained lightweight version using Python and SQLite:

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start Application
```bash
python app.py
```

### 3. Access in Browser
Navigate to: **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

*(The standalone app automatically provisions a local `votes.db` SQLite database).*

---

## 🛠 Essential Docker Commands

### Check Service Status
```bash
docker compose ps
```

### Stream Live Logs
```bash
# All services
docker compose logs -f

# Backend service only
docker compose logs -f backend

# Database service only
docker compose logs -f db

# Frontend Nginx only
docker compose logs -f frontend
```

### Inspect Database with `psql` CLI
```bash
docker compose exec db psql -U postgres -d voting_db
```
Useful SQL queries inside `psql`:
```sql
-- View all votes:
SELECT * FROM votes;

-- View aggregated tally:
SELECT party, COUNT(*) FROM votes GROUP BY party;

-- Exit:
\q
```

### Stop Services
```bash
# Stop containers (preserves database data in volume)
docker compose down

# Stop and purge database volume (fresh start)
docker compose down -v
```

---

## 🌟 Star History

If you found this project helpful, please give it a ⭐ **Star** on GitHub to show support!

<div align="center">
  <a href="https://star-history.com/#Jani-shiv/Voting-Docker-image&Date">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=Jani-shiv/Voting-Docker-image&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=Jani-shiv/Voting-Docker-image&type=Date" />
      <img alt="Voting-Docker-image Star History Chart" src="https://api.star-history.com/svg?repos=Jani-shiv/Voting-Docker-image&type=Date" width="100%" />
    </picture>
  </a>
</div>

---

## 📂 Project Directory Structure

```plaintext
Voting-Docker-image/
├── .dockerignore                 # Docker build exclusion rules
├── .gitignore                    # Git tracking ignore rules
├── LICENSE                       # MIT License
├── README.md                     # Comprehensive documentation
├── DOCKER_PRACTICE.md            # Interactive Docker exercises & commands guide
├── flow.md                       # Application architectural request/response flow
├── docker-compose.yml            # 3-Tier multi-container orchestration spec
├── Dockerfile                    # Standalone single-container Dockerfile
├── requirements.txt              # Standalone Python dependencies (Flask)
├── app.py                        # Standalone Flask application with SQLite
│
├── backend/                      # Decoupled Backend Microservice
│   ├── Dockerfile                # Python 3.12-slim backend container spec
│   ├── requirements.txt          # Backend dependencies (Flask, psycopg2, gunicorn)
│   └── app.py                    # Flask API with PostgreSQL integration & retries
│
├── frontend/                     # Frontend Microservice & Reverse Proxy
│   ├── Dockerfile                # Nginx Alpine container spec
│   ├── nginx.conf                # Custom Nginx reverse proxy configuration
│   └── html/                     # Static UI assets served by Nginx
│       ├── index.html            # Bento-grid voting interface
│       ├── style.css             # Utilitarian brutalist styling
│       └── app.js                # Async client-side API logic
│
├── static/                       # Static assets for standalone Flask app
│   ├── style.css
│   └── app.js
│
└── templates/                    # Jinja2 templates for standalone Flask app
    └── index.html
```

---

## 👨‍💻 Author & Connect

<div align="center">

<a href="https://github.com/Jani-shiv">
  <img src="https://avatars.githubusercontent.com/u/153932136?v=4" width="110" height="110" style="border-radius: 50%;" alt="Shiv Jani Avatar" />
</a>

### **Shiv Jani**
*DevOps Engineer & Linux Practitioner*

Passionate about Linux, CI/CD, container orchestration, and reliable cloud-native infrastructure.

[![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Connect%20%26%20Follow-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/shiv-jani/)
[![GitHub Follow](https://img.shields.io/badge/GitHub-Follow%20%40Jani--shiv-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Jani-shiv)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20Website-4F46E5?style=for-the-badge&logo=google-chrome&logoColor=white)](https://itsme-gold.vercel.app)
[![YouTube](https://img.shields.io/badge/YouTube-DevOpsNi%20Diary-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@devopsnidiary)

</div>

---

## 📜 License

This project is open source and distributed under the [MIT License](./LICENSE). Feel free to adapt, practice, and extend!
