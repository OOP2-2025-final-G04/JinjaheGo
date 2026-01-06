from flask import Blueprint, render_template, request, redirect, url_for, jsonify # jsonifyを追加
import os
import json
import random

saisen_bp = Blueprint('saisen', __name__)

@saisen_bp.route('/saisen', methods=['GET', 'POST'])
def saisen():
    # URLパラメータから神社IDを取得
    jinja_id = request.args.get('jinja')
    # ポイントファイルの絶対パスを取得
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
    
    # POSTリクエスト時（お賽銭が入った時）
    if request.method == 'POST':
        # 1〜5ポイントをランダムで加算
        add_pt = random.randint(1, 5)
        point += add_pt
        
        try:
            # ポイントファイルに書き込み（JSON形式）
            with open(point_file, 'w', encoding='utf-8') as f:
                json.dump({'point': point}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass # 書き込みエラー時は無視
        
        # JSON形式でレスポンスを返す（獲得ポイント、現在ポイント、リダイレクト先URL）
        return jsonify({
            'add_pt': add_pt,
            'current_total': point,
            'redirect_url': url_for('choose.choose', jinja=jinja_id)
        })
    # GETリクエスト以外（POSTなど）も考慮してレンダリング
    return render_template('saisen.html', jinja_id=jinja_id, point=point, get_point=0)