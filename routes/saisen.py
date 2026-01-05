
from flask import Blueprint, render_template, request, redirect, url_for
import os
import json
import random

# Blueprintの作成
saisen_bp = Blueprint('saisen', __name__)


@saisen_bp.route('/saisen', methods=['GET', 'POST'])
def saisen():
    jinja_id = request.args.get('jinja') # クエリパラメータからjinjaのidを取得
    point_file = os.path.join(os.path.dirname(__file__), '../point.json')
    point_file = os.path.abspath(point_file)
    # ポイントの初期値
    point = 0
    # point.jsonの読み込み
    if os.path.exists(point_file):
        try:
            with open(point_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                point = data.get('point', 0)
        except Exception:
            point = 0
    
    # POSTリクエスト時：ポイントを増加する
    if request.method == 'POST':
        # 1~5ptをランダム加算
        add_pt = random.randint(1, 5)
        point += add_pt
        # point.jsonに保存
        try:
            with open(point_file, 'w', encoding='utf-8') as f:
                json.dump({'point': point}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
        return redirect(url_for('saisen.saisen', jinja=jinja_id)) # POSTしても、jinjaのidは持たせておく
    
    # GETリクエスト時: 画面表示
    return render_template('saisen.html', jinja_id=jinja_id, point=point)
