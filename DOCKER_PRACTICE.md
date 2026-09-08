# Docker Compose 3-Container Practice Guide

This guide walks you through practicing multi-container orchestration with **Docker Compose** using a complete 3-tier architecture:

```
[ Browser: http://localhost:8085 ]
               │
               ▼
   [ frontend (Nginx Web Server) ]  ─── port 80
               │
               │ (internal Docker network: http://backend:5000/api/)
               ▼
   [ backend (Flask API) ]          ─── port 5000
               │
               │ (internal Docker network: db:5432)
               ▼
   [ db (PostgreSQL Database) ]     ─── port 5432 (volume: postgres_data)
```

---

## 1. Quick Start Commands

### Step 1: Build and Start All 3 Containers
Run this command from the project root (`Python app`):
```bash
docker compose up --build
```
> Add `-d` to run in the background (detached mode):
> ```bash
> docker compose up --build -d
> ```

### Step 2: Open the Application
- Open your web browser and go to: **[http://localhost:8085](http://localhost:8085)**
- Enter a voter name, select a character card (e.g. *Oggy*, *Sinchan*), and click **"Cast Your Vote"**.
- Notice the standings update live!

---

## 2. Docker Compose Commands to Practice

### 1. View Status of All Services
```bash
docker compose ps
```
You will see 3 services running:
- `voting_db` (status: `healthy`)
- `voting_backend` (status: `running`)
- `voting_frontend` (status: `running`)

---

### 2. View Live Logs

View combined logs from all 3 containers:
```bash
docker compose logs -f
```

View logs for only one specific container:
```bash
# Only backend logs
docker compose logs -f backend

# Only database logs
docker compose logs -f db

# Only frontend (Nginx) logs
docker compose logs -f frontend
```

---

### 3. Execute Commands Inside Containers (`docker compose exec`)

#### Inspect Database Directly via SQL:
Run PostgreSQL's interactive CLI (`psql`) directly inside the database container:
```bash
docker compose exec db psql -U postgres -d voting_db
```
Inside the `psql` prompt:
```sql
-- List tables:
\dt

-- View cast votes:
SELECT * FROM votes;

-- View vote summary:
SELECT party, COUNT(*) FROM votes GROUP BY party;

-- Exit psql:
\q
```

#### Test Backend from Inside the Container:
```bash
docker compose exec backend python -c "import psycopg2; print('Python DB driver ready!')"
```

#### Inspect Nginx Configuration in Frontend:
```bash
docker compose exec frontend cat /etc/nginx/conf.d/default.conf
```

---

### 4. Test Service Discovery and Networking

Inside Docker Compose, each container can communicate using the service name as the hostname:
- `frontend` talks to `http://backend:5000`
- `backend` talks to `db:5432`

You can test network connectivity between containers:
```bash
# Ping db from backend container
docker compose exec backend ping -c 2 db
```

---

### 5. Stopping and Restarting

#### Stop containers without losing database data:
```bash
docker compose stop
```

#### Start stopped containers again:
```bash
docker compose start
```

#### Tear down containers and networks:
```bash
docker compose down
```
*(Your votes in the database will still be saved inside the `postgres_data` volume).*

#### Complete Reset (Deletes database data too):
```bash
docker compose down -v
```

---

## 3. Architecture Deep-Dive for Practice

| Service | Technology | Role | How It Connects |
|---|---|---|---|
| **`frontend`** | Nginx Alpine | Serves static HTML/CSS/JS files and acts as a reverse proxy | Browser calls port `8080`. Nginx serves UI and forwards `/api/*` to `backend:5000` |
| **`backend`** | Python 3.12 + Flask | Handles business logic and voting API endpoints | Listens on port `5000`. Connects to `db:5432` using `psycopg2` |
| **`db`** | PostgreSQL 16 Alpine | Relational database storing votes persistently | Listens on port `5432`. Data is stored in Docker volume `postgres_data` |

---

## 4. Docker Hub Images

Your custom images are published and publicly available on Docker Hub:

- **Frontend**: [`jani712/voting-frontend:latest`](https://hub.docker.com/r/jani712/voting-frontend)
  ```bash
  docker pull jani712/voting-frontend:latest
  ```

- **Backend**: [`jani712/voting-backend:latest`](https://hub.docker.com/r/jani712/voting-backend)
  ```bash
  docker pull jani712/voting-backend:latest
  ```

- **Database**:
  Uses official [`postgres:16-alpine`](https://hub.docker.com/_/postgres) image.

---

Happy Docker Compose practicing!
