import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template
from models.models import db, User
from models.omikuji import OmikujiHistory
from routes.omikuji import omikuji_bp

app = Flask(__name__)

# ★ DB初期化（OK）
db.connect()
db.create_tables([User, OmikujiHistory])

# ★ Blueprint登録
app.register_blueprint(omikuji_bp)

@app.route("/")
def index():
    history = (
        OmikujiHistory
        .select()
        .order_by(OmikujiHistory.created_at.desc())
        .limit(10)
    )
    return render_template(
        "omikuji.html",
        point=100,
        history=history
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
