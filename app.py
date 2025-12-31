from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open('articles.json', 'r') as f:
            articles_data = json.load(f)
    except:
        articles_data = {"total_articles": 0}
    
    articles_list = ""
    for key in articles_data:
        if key.startswith("article"):
            art = articles_data[key]
            alaune = "🔥" if art.get("alaune") == "oui" else ""
            articles_list += f'<div><h3>{alaune}<a href="/blog/{art["lien"]}">{art["titre"]}</a></h3><p>{art["contenu"][:100]}...</p></div><hr>'
    
    return f'''
    <h1>Perspectives Actuelles</h1>
    <p>Articles: {articles_data.get("total_articles", 0)} | 
    <a href="/articles">JSON</a> | <a href="/users">Users</a></p>
    <hr>
    {articles_list}
    '''

@app.route("/articles")
def get_articles():
    try:
        with open('articles.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "articles.json manquant"})

@app.route("/users")
def get_users():
    try:
        with open('users.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({"error": "users.json manquant"})

@app.route('/blog/<path:filename>')
def serve_blog(filename):
    try:
        with open(f'blog/{filename}', 'r') as f:
            return f.read()
    except:
        return "404 - Article non trouvé", 404

@app.route('/blog/img/<path:filename>')
def serve_img(filename):
    try:
        with open(f'blog/img/{filename}', 'rb') as f:
            return f.read()
    except:
        return "Image non trouvée", 404

@app.route("/a-la-une")
def alaune():
    try:
        with open('articles.json', 'r') as f:
            data = json.load(f)
        une = {k:v for k,v in data.items() if k.startswith('article') and v.get('alaune')=='oui'}
        return jsonify({"a_la_une": une})
    except:
        return jsonify({"error": "articles.json manquant"})


if __name__ == "__main__":
    app.run(debug=True)
