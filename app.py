import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template

from models.models import initialize_database
from routes import blueprints
from models.models import db, User
from models.omikuji import OmikujiHistory
from routes.omikuji import omikuji_bp

app = Flask(__name__)

# ★ DB初期化（OK）
db.connect()
db.create_tables([User, OmikujiHistory])

# ★ Blueprint登録
app.register_blueprint(omikuji_bp)

# Blueprint登録
for bp in blueprints:
    app.register_blueprint(bp)

@app.route("/")
def index():
    return render_template("index.html")

    # ===== TODO: routes/omikuji.py =====
    history = (
        OmikujiHistory.select().order_by(OmikujiHistory.created_at.desc()).limit(10)
    )
    return render_template("omikuji.html", point=100, history=history)


# 神社ごとの処理
# 例: /shrine/ise にアクセスが来たらここが動く
@app.route("/shrine/<name>")
def shrine_omikuji(name):
    # name には "ise", "izumo", "itsukushima" が入ります

    # ここで「伊勢神宮なら大吉が出やすい」みたいな特別処理も書けます！
    if name == "ise":
        display_name = "伊勢神宮"
    elif name == "izumo":
        display_name = "出雲大社"
    elif name == "nikko":
        display_name = "日光東照宮"
    else:
        display_name = "謎の神社"

    return render_template("result.html", shrine_name=display_name)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
