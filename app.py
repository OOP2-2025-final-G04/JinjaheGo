from flask import Flask, render_template
from models.models import initialize_database
from routes.choose import choose_bp

app = Flask(__name__)

initialize_database()

app.register_blueprint(choose_bp)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose")
def choose():
    points = 0  # 仮のポイント値
    return render_template("choose.html", points=points)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
