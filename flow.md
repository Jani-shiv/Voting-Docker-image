# 🔄 Voting Machine Application Flow & Execution Architecture

This document details the internal request lifecycles, service interactions, and data flows for both the **Single-Node Standalone Architecture** and the **Multi-Container Microservice Architecture**.

---

## 1. Multi-Container Microservices Flow (Docker Compose)

### 1.1 Architectural Topology
```
[ Client Browser ]
        │
        │ HTTP GET/POST :8085
        ▼
[ voting_frontend (Nginx) ]
   ├── Static assets (/ -> /usr/share/nginx/html)
   └── API reverse proxy (/api/* -> http://backend:5000/api/*)
        │
        │ Internal Docker Network (voting_network)
        ▼
[ voting_backend (Flask) ]
   ├── /api/health  -> JSON health response
   ├── /api/vote    -> Validate & INSERT query
   └── /api/results -> SELECT & GROUP BY query
        │
        │ TCP: 5432 (psycopg2-binary)
        ▼
[ voting_db (PostgreSQL 16) ]
   └── Table: votes (persisted in volume: voting_postgres_data)
```

### 1.2 Step-by-Step Lifecycle

#### A. Initial Page Load (`GET /`)
1. The browser requests `http://localhost:8085/`.
2. **Nginx** handles the request directly and returns `index.html` from `/usr/share/nginx/html`.
3. The browser requests `./style.css` and `./app.js`; Nginx returns both static files with optimal caching.
4. As `app.js` runs, it executes `fetchResults()` asynchronously.
5. `app.js` sends an HTTP `GET /api/results`.
6. Nginx intercepts `/api/results` and reverse-proxies it to `http://backend:5000/api/results`.
7. **Flask** queries PostgreSQL:
   ```sql
   SELECT party, COUNT(*) as count FROM votes GROUP BY party;
   ```
8. Flask returns a JSON object with counts for all parties (`Oggy`, `Hathori`, `Doremon`, `Sinchan`).
9. JavaScript updates the DOM standings in real time.

#### B. Casting a Vote (`POST /api/vote`)
1. The user inputs their name and selects a candidate card.
2. The user clicks **"Cast Your Vote"**.
3. JavaScript locks the submit button to prevent double-submissions.
4. `app.js` issues a `POST` request to `/api/vote`:
   ```json
   {
     "name": "Bruce Wayne",
     "party": "Sinchan"
   }
   ```
5. Nginx forwards the payload to Flask.
6. Flask validates required fields and executes:
   ```sql
   INSERT INTO votes (name, party) VALUES (%s, %s);
   ```
7. Database commits transaction and returns success.
8. Flask returns `{"success": true, "message": "Vote cast successfully!"}`.
9. Frontend clears input fields, displays a success toast, and immediately triggers `fetchResults()` to update the live standings.

---

## 2. Database Schema (PostgreSQL)

```sql
CREATE TABLE IF NOT EXISTS votes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    party VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. Standalone Mode Flow (SQLite)

In local developer mode without Docker:
- **Web Server & API**: Single Flask process on `http://127.0.0.1:5000`.
- **Template Rendering**: Flask `render_template('index.html')` serves the HTML.
- **Database**: SQLite file (`votes.db`) created locally in the root folder.
