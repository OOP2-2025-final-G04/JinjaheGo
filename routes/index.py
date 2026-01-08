from flask import Blueprint, render_template
import os
import json

# Blueprintの作成
index_bp = Blueprint('index', __name__)

def get_current_points():
    """
    point.json から現在のポイントを読み込む関数
    (saisen.py のロジックを流用)
    """
    # 現在のファイル(index.py)の1つ上の階層にある point.json を探す
    point_file = os.path.join(os.path.dirname(__file__), '../point.json')
    point_file = os.path.abspath(point_file)
    
    point = 0
    
    # ファイルが存在すれば読み込み
    if os.path.exists(point_file):
        try:
            with open(point_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                point = data.get('point', 0)
        except Exception:
            # 読み込みエラー（ファイル破損など）時は0にする
            point = 0
            
    return point

@index_bp.route('/')
def index():
    # ポイントを取得
    points = get_current_points()
    
    # 画面(index.html)にポイントを渡して表示
    return render_template('index.html', points=points)