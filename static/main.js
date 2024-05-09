function fetchAndUpdate() {
    fetch('/value')
        .then(response => response.text())
        .then(data => {
            document.getElementById('value').innerHTML = 'Float value: ' + data;
        });
}
fetchAndUpdate();
setInterval(fetchAndUpdate, 1000);
