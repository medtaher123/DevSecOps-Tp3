"""Notes API used as the TP3 container target.

The API key is read from the environment. It is never written into the image.
"""

import os
import sqlite3

from flask import Flask, request
from markupsafe import escape

app = Flask(__name__)
DB = os.environ.get("DB_PATH", "/tmp/users.db")
API_KEY = os.environ.get("API_KEY", "")


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users "
        "(id INTEGER PRIMARY KEY, name TEXT, password TEXT)"
    )
    conn.execute("DELETE FROM users")
    conn.execute(
        "INSERT INTO users (name, password) VALUES (?, ?)",
        ("admin", "admin123"),
    )
    conn.commit()
    conn.close()


@app.route("/")
def index():
    return (
        "<h1>Notes API</h1>"
        '<a href="/user?name=admin">user</a> '
        '<a href="/hello?name=test">hello</a> '
        '<a href="/status">status</a>'
    )


@app.route("/user")
def get_user():
    name = request.args.get("name", "")
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        "SELECT id, name FROM users WHERE name = ?",
        (name,),
    ).fetchall()
    conn.close()
    return {"users": [{"id": r[0], "name": r[1]} for r in rows]}


@app.route("/hello")
def hello():
    name = request.args.get("name", "inconnu")
    return f"<h1>Bonjour {escape(name)}</h1>"


@app.route("/status")
def status():
    # Prove the secret is present without printing it.
    return {
        "secret_configured": bool(API_KEY),
        "secret_length": len(API_KEY),
    }


if __name__ == "__main__":
    init_db()
    host = os.environ.get("APP_HOST", "127.0.0.1")
    app.run(host=host, port=5000, debug=False)
