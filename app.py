import json
import sys
import os

# 現在のディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template

from routes import blueprints
from models.models import db, User
from models.omikuji import OmikujiHistory
from routes.omikuji import omikuji_bp
from routes.choose import choose_bp
from routes.index import index_bp # もしindex.pyがない場合は削除してください

app = Flask(__name__)

# ★ DB初期化
db.connect()
db.create_tables([User, OmikujiHistory])

# ★ Blueprint登録
# index_bpがある場合は登録、なければコメントアウト
# app.register_blueprint(index_bp) 

app.register_blueprint(omikuji_bp)

for bp in blueprints:
    app.register_blueprint(bp)

app.register_blueprint(choose_bp)

def get_current_points():
    # point.json の絶対パスを取得
    point_file = os.path.join(os.path.dirname(__file__), 'point.json')
    point_file = os.path.abspath(point_file)
    
    point = 0
    
    if os.path.exists(point_file):
        try:
            with open(point_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                point = data.get('point', 0)
        except Exception:
            point = 0
            
    return point

@app.route("/")
def index():
    # ポイントを取得して画面に渡す
    points = get_current_points()
    return render_template("index.html", points=points)


@app.route("/shrine/<name>")
def shrine_omikuji(name):
    # 結果画面でもポイントを表示
    points = get_current_points()

    if name == "ise":
        display_name = "伊勢神宮"
    elif name == "izumo":
        display_name = "出雲大社"
    elif name == "nikko":
        display_name = "日光東照宮"
    else:
        display_name = "謎の神社"

    return render_template("result.html", shrine_name=display_name, points=points)


@app.route("/choose")
def choose():
    points = get_current_points()
    return render_template("choose.html", points=points)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)