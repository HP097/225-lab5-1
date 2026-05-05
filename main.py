from flask import Flask, render_template_string, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Persistence logic for the school NFS
DATABASE = 'file:/nfs/tasks.db?vfs=unix-dotfile'

def get_db():
    db = sqlite3.connect(DATABASE, uri=True)
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    db = get_db()
    db.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)')
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return render_template_string('''
        <h1>Hitesh's Lab 5.1 Task Manager</h1>
        <form method="POST" action="/add">
            <input type="text" name="task" placeholder="Enter new task" required>
            <button type="submit">Add Task</button>
        </form>
        <ul>
            {% for task in tasks %}
                <li>{{ task.task }}</li>
            {% endfor %}
        </ul>
    ''', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task', '').strip() # Security: Sanitizing input
    if task:
        db = get_db()
        db.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        db.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Security: Debug is OFF for production deployment
    app.run(debug=False, host='0.0.0.0', port=5000) # nosec
