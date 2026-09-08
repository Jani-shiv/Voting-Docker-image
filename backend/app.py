import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "voting_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db(max_retries=10, retry_delay=2):
    """Wait for PostgreSQL to be ready and create tables."""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"[Backend] Connecting to PostgreSQL at {DB_HOST}:{DB_PORT} (attempt {attempt}/{max_retries})...")
            conn = get_db_connection()
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS votes (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        party VARCHAR(100) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                ''')
            conn.commit()
            conn.close()
            print("[Backend] Database initialized successfully.")
            return
        except Exception as e:
            print(f"[Backend] DB connection attempt {attempt} failed: {e}")
            if attempt < max_retries:
                time.sleep(retry_delay)
            else:
                print("[Backend] Could not connect to database after maximum retries.")

# Initialize the database table on startup
init_db()

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'backend'})

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.get_json(silent=True) or {}
    name = data.get('name')
    party = data.get('party')

    if not name or not party:
        return jsonify({'error': 'Name and party are required'}), 400

    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("INSERT INTO votes (name, party) VALUES (%s, %s)", (name, party))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Vote cast successfully!'})
    except Exception as e:
        print(f"Error inserting vote: {e}")
        return jsonify({'error': 'Failed to save vote'}), 500

@app.route('/api/results', methods=['GET'])
def results():
    results_dict = {
        'Oggy': 0,
        'Hathori': 0,
        'Doremon': 0,
        'Sinchan': 0
    }
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT party, COUNT(*) as count FROM votes GROUP BY party")
            rows = cur.fetchall()
            for party, count in rows:
                if party in results_dict:
                    results_dict[party] = count
                else:
                    results_dict[party] = count
        conn.close()
        return jsonify(results_dict)
    except Exception as e:
        print(f"Error fetching results: {e}")
        return jsonify(results_dict), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
