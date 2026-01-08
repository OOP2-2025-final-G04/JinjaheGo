import json
import os
from flask import Blueprint, render_template, jsonify
from models.omikuji import OmikujiHistory
import random

omikuji_bp = Blueprint('omikuji', __name__)

POINT_FILE = "point.json"
OMIKUJI_COST = 5


def load_point():
    with open(POINT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)["point"]


def save_point(point):
    with open(POINT_FILE, "w", encoding="utf-8") as f:
        json.dump({"point": point}, f, ensure_ascii=False, indent=2)


# ===== おみくじロジック =====

def rand_mark():
    return random.choice(['◎','○','△','×'])

def score(mark):
    return {'◎':3, '○':2, '△':1, '×':0}[mark]

def calc_fortune(marks):
    total = sum(score(m) for m in marks)
    if total >= 12: return '大吉'
    if total >= 10: return '中吉'
    if total >= 7:  return '小吉'
    if total >= 5:  return '吉'
    if total >= 3:  return '末吉'
    return '凶'

# ===== 一言コメント定義 =====

COMMENTS = {
    "wish": {
        "◎": "必ず叶う",
        "○": "努力次第で叶う",
        "△": "時を待て",
        "×": "叶い難し"
    },
    "lost": {
        "◎": "見つかる",
        "○": "探せば見つかる",
        "△": "時間がかかる",
        "×": "諦めよ"
    },
    "wait": {
        "◎": "必ず来る",
        "○": "来る見込みあり",
        "△": "遅れて来る",
        "×": "来ず"
    },
    "health": {
        "◎": "万事快調",
        "○": "概ね良し",
        "△": "無理禁物",
        "×": "注意せよ"
    },
    "study": {
        "◎": "大いに伸びる",
        "○": "努力が実る",
        "△": "油断するな",
        "×": "怠れば失う"
    }
}

def with_comment(category, mark):
    return f"{mark} {COMMENTS[category][mark]}"

# ===== 画面表示 =====

@omikuji_bp.route('/omikuji')
def omikuji_page():
    history = (
        OmikujiHistory
        .select()
        .order_by(OmikujiHistory.created_at.desc())
        .limit(10)
    )
    return render_template('omikuji.html', history=history, point=0)

# ===== おみくじ実行 =====

@omikuji_bp.route('/draw_omikuji', methods=['POST'])
def draw_omikuji():
    current_point = load_point()

    # ポイント不足チェック
    if current_point < OMIKUJI_COST:
        return jsonify({
            "error": "ポイントが足りません",
            "point": current_point
        })

    # ポイント消費
    current_point -= OMIKUJI_COST
    save_point(current_point)

    # ===== ここからおみくじ処理（今まで通り） =====
    wish = rand_mark()
    lost = rand_mark()
    wait = rand_mark()
    health = rand_mark()
    study = rand_mark()

    marks = [wish, lost, wait, health, study]
    fortune = calc_fortune(marks)

    OmikujiHistory.create(
        fortune=fortune,
        wish=wish,
        lost=lost,
        wait=wait,
        health=health,
        study=study
    )

    history = (
        OmikujiHistory
        .select()
        .order_by(OmikujiHistory.created_at.desc())
        .limit(10)
    )

    history_list = []
    for h in history:
        history_list.append({
            'fortune': h.fortune,
            'wish': h.wish,
            'lost': h.lost,
            'wait': h.wait,
            'health': h.health,
            'study': h.study,
            'time': h.created_at.strftime('%m/%d %H:%M')
        })

    return jsonify({
        "fortune": fortune,
        "wish": with_comment("wish", wish),
        "lost": with_comment("lost", lost),
        "wait": with_comment("wait", wait),
        "health": with_comment("health", health),
        "study": with_comment("study", study),
        "history": history_list,
        "point": current_point
    })