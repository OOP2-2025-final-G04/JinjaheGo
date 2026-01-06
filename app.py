from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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
