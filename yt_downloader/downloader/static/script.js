document.getElementById('download-button').addEventListener('click', function() {
    document.getElementById('format-section').style.display = 'block';
});

document.getElementById('format-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('url-input').value;
    const format = document.getElementById('format').value;
    const quality = document.getElementById('quality').value;

    fetch('/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url, format, quality })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.downloadLink;
        } else {
            alert('Error: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
});
