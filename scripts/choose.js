document.addEventListener('DOMContentLoaded', function() {
    fetch('/static/point.json')
        .then(response => response.json())
        .then(data => {
            const points = data.points;
            document.querySelector('.points').textContent = 'ポイント: ' + points;
            localStorage.setItem('points', points);
        })
        .catch(error => console.error('Error fetching points:', error));
});