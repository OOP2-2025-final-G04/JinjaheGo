from flask import Flask, render_template
from models.models import initialize_database
from routes import blueprints

app = Flask(__name__)

initialize_database()

# Blueprint登録
for bp in blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
