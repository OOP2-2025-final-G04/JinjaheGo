from flask import Blueprint, redirect, url_for

choose_bp = Blueprint("choose", __name__)

# 賽銭を投げる → 他メンバーの画面へ
@choose_bp.route("/offer", methods=["POST"])
def go_offer_screen():
    return redirect(url_for("offer_screen"))


# 御神籤を引く → 別の画面へ
@choose_bp.route("/omikuji", methods=["POST"])
def go_omikuji_screen():
    return redirect(url_for("omikuji_screen"))


# 地図に戻る
@choose_bp.route("/back_to_map")
def back_to_map():
    return redirect(url_for("map"))