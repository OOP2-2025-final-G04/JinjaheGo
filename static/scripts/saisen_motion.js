// 五円玉投げ入れアニメーション制御
window.addEventListener('DOMContentLoaded', function() {
    // 五円玉、賽銭箱、ポイント表示用の要素を取得
    const goen = document.querySelector('.goen');
    const saisenbako = document.querySelector('.saisenbako');
    const pointDisplay = document.querySelector('.point-result');
    let isThrown = false; // すでに投げ入れられたかどうかのフラグ

    let startX, startY, initialX, initialY; // ドラッグ開始座標と初期位置変位の変数

    // ドラッグ開始イベント（タッチまたはマウスダウン）を登録
    goen.addEventListener('touchstart', onStart, { passive: false });
    goen.addEventListener('mousedown', onStart);

    // ドラッグ開始時の処理（mousedown / touchstart）
    function onStart(e) {
        if (isThrown) return; // 既に投げ入れ済みの場合は何もしない
        e.preventDefault(); // デフォルトの動作（画像ドラッグなど）を防ぐ

        const event = e.type === 'mousedown' ? e : e.touches[0]; // マウスかタッチか判定
        startX = event.clientX; // 開始時のX座標
        startY = event.clientY; // 開始時のY座標

        // 現在のtransform値を取得（前回の位置情報を保持するため）
        const style = window.getComputedStyle(goen);
        const matrix = new WebKitCSSMatrix(style.transform);
        initialX = matrix.m41; // 現在のX変位量
        initialY = matrix.m42; // 現在のY変位量

        // ドラッグ移動中と終了時のイベントリスナーを追加
        document.addEventListener('touchmove', onMove, { passive: false });
        document.addEventListener('touchend', onEnd);
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onEnd);
    }

    // ドラッグ移動中の処理（mousemove / touchmove）
    function onMove(e) {
        if (isThrown) return; // 既に投げ入れ済みの場合は何もしない
        e.preventDefault(); // デフォルトのスクロールなどを防ぐ
        const event = e.type === 'mousemove' ? e : e.touches[0]; // マウスかタッチか判定
        const dx = event.clientX - startX; // 開始位置からのX移動量
        const dy = event.clientY - startY; // 開始位置からのY移動量
        // 初期位置(initialX/Y)に移動量(dx/dy)を加えて移動させる
        goen.style.transform = `translate(${initialX + dx}px, ${initialY + dy}px)`;
    }

    // ドラッグ終了時の処理（mouseup / touchend）
    function onEnd(e) {
        // 各種イベントリスナーを解除してリソースを解放
        document.removeEventListener('touchmove', onMove);
        document.removeEventListener('touchend', onEnd);
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onEnd);

        // 五円玉と賽銭箱が重なっているか判定
        if (checkCollision(goen, saisenbako)) {
            successThrow(); // 重なっていれば成功処理へ
        } else {
            // 重なっていなければ元の位置に戻すアニメーション
            goen.style.transition = 'transform 0.3s ease';
            goen.style.transform = 'translate(0px, 0px)';
            // アニメーション終了後にtransition設定を解除（次の動作のため）
            setTimeout(() => { goen.style.transition = ''; }, 300);
        }
    }

    // 2つの要素が重なっているか判定する関数
    function checkCollision(el1, el2) {
        const r1 = el1.getBoundingClientRect(); // 要素1の位置・サイズ取得
        const r2 = el2.getBoundingClientRect(); // 要素2の位置・サイズ取得
        // 矩形同士が重なっていない条件の逆（つまり重なっている）を返す
        return !(r1.right < r2.left || r1.left > r2.right || r1.bottom < r2.top || r1.top > r2.bottom);
    }

    // ドロップ判定された後の処理
    function successThrow() {
        if (isThrown) return; // 既に投げ入れ済みの場合は何もしない
        isThrown = true; // 投げ入れフラグをオンにする
        goen.style.display = 'none'; // 五円玉画像を非表示にする
        
        // サーバーにPOSTリクエストを送信して結果を取得
        fetch(window.location.href, { method: 'POST' })
        .then(response => response.json()) // レスポンスをJSONとしてパース
        .then(data => {
            // サーバーから返ってきた獲得ポイントを表示
            pointDisplay.innerText = `${data.add_pt} pt 獲得！`;
            pointDisplay.style.display = 'block'; // ポイント結果を表示
            // 2秒後に指定されたURLへ遷移
            setTimeout(function() {
                window.location.href = data.redirect_url;
            }, 2000);
        })
        .catch(error => console.error('Error:', error)); // エラーが発生した場合はログに出力
    }
});