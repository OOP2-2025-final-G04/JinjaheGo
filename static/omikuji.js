document.addEventListener("DOMContentLoaded", () => {

    const drawBtn = document.getElementById("draw-btn");
    const resultDiv = document.getElementById("result");
    const historyUl = document.getElementById("history");

    const box = document.getElementById("box");
    const paper = document.getElementById("paper");

    const fortune = document.getElementById("fortune");
    const wish = document.getElementById("wish");
    const lost = document.getElementById("lost");
    const wait = document.getElementById("wait");
    const health = document.getElementById("health");
    const study = document.getElementById("study");

    drawBtn.addEventListener("click", async () => {

        // 箱を揺らす
        box.classList.add("shake");

        setTimeout(() => {
            box.classList.remove("shake");
            paper.classList.remove("hidden");
        }, 600);

        // おみくじ取得
        const response = await fetch("/draw_omikuji", { method: "POST" });
        const data = await response.json();

        // 結果表示
        resultDiv.textContent = `結果：${data.fortune}`;
        fortune.textContent = data.fortune;
        wish.textContent = data.wish;
        lost.textContent = data.lost;
        wait.textContent = data.wait;
        health.textContent = data.health;
        study.textContent = data.study;

        // 履歴更新
        historyUl.innerHTML = "";

        data.history.forEach(item => {
            const li = document.createElement("li");
            li.classList.add("history-item");

            li.innerHTML =
                `<div class="history-time">${item.time}　${item.fortune}</div>` +
                `<div class="history-detail">` +
                `願い事：${item.wish} ` +
                `失せ物：${item.lost} ` +
                `待ち人：${item.wait} ` +
                `健康：${item.health} ` +
                `学問：${item.study}` +
                `</div>`;

            historyUl.appendChild(li);
        });
    });
});
