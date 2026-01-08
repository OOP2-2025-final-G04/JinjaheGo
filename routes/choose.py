from flask import Blueprint, redirect, url_for, render_template, request

import json
import os
choose_bp = Blueprint("choose", __name__)


# 選択画面を表示
@choose_bp.route("/choose")
def choose():
    jinja_id = request.args.get("jinja")
    point_file = os.path.join(os.path.dirname(__file__), '../point.json')
    point_file = os.path.abspath(point_file)
    
    # ポイントファイル（point.json）の読み込み処理
    # ファイルが存在すれば読み込み、なければ初期値0とする
    point = 0
    if os.path.exists(point_file):
        try:
            with open(point_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                point = data.get('point', 0)
        except Exception:
            point = 0

    return render_template("choose.html", jinja_id=jinja_id, points=point)


# 賽銭を投げる → 他メンバーの画面へ
@choose_bp.route("/offer", methods=["POST"])
def go_offer_screen():
    return redirect(url_for("choose.go_offer_screen"))


# 御神籤を引く → 別の画面へ
@choose_bp.route("/omikuji", methods=["POST"])
def go_omikuji_screen():
    return redirect(url_for("choose.go_omikuji_screen"))


# 地図に戻る
@choose_bp.route("/back_to_map")
def back_to_map():
    return redirect(url_for("map"))
    # return redirect(url_for("choose.back_to_map"))
