from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    init_db()
    return '''
    <h1>Perspectives Actuelles - Jour 2</h1>
    <p><a href="/articles">Articles JSON</a> | 
    <a href="/users">Users JSON</a></p>
    <p>SQLite DB OK ! Tables: articles(2) + users(2)</p>
    '''

@app.route("/articles")
def get_articles():
    conn = get_db_connection()
    articles = [{"id": row['id'], "title": row['title'], "content": row['content'], "date": row['date']} 
                for row in conn.execute('SELECT * FROM articles').fetchall()]
    conn.close()
    return jsonify(articles)

@app.route("/users")
def get_users():
    conn = get_db_connection()
    users = [{"id": row['id'], "name": row['name'], "email": row['email'], "role": row['role']} 
             for row in conn.execute('SELECT * FROM users').fetchall()]
    conn.close()
    return jsonify(users)

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS articles')
    c.execute('DROP TABLE IF EXISTS users')
    c.execute('''CREATE TABLE articles (id INTEGER PRIMARY KEY, title TEXT, content TEXT, date TEXT)''')
    c.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT, role TEXT)''')
    
    c.execute("INSERT INTO articles VALUES (1, 'Article 111', 'Sprint 2 OK', '2025-12-28')")
    c.execute("INSERT INTO articles VALUES (2, 'Article 112', 'IA APIs OK', '2025-12-28')")
    c.execute("INSERT INTO users VALUES (1, 'David', 'david@example.com', 'admin')")
    c.execute("INSERT INTO users VALUES (2, 'Test', 'test@example.com', 'user')")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    app.run(debug=True)
