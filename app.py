import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
DB_FILE = 'votes.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            party TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vote', methods=['POST'])
def vote():
    data = request.json
    name = data.get('name')
    party = data.get('party')

    if not name or not party:
        return jsonify({'error': 'Name and party are required'}), 400

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Check if user already voted (optional feature for realism, let's keep it simple as requested)
    c.execute("INSERT INTO votes (name, party) VALUES (?, ?)", (name, party))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Vote cast successfully!'})

@app.route('/api/results', methods=['GET'])
def results():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Query to count votes for each party
    c.execute("SELECT party, COUNT(*) as count FROM votes GROUP BY party")
    rows = c.fetchall()
    
    # Format results
    results_dict = {
        'Oggy': 0,
        'Hathori': 0,
        'Doremon': 0,
        'Sinchan': 0
    }
    
    for row in rows:
        if row[0] in results_dict:
            results_dict[row[0]] = row[1]
            
    conn.close()
    
    return jsonify(results_dict)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)