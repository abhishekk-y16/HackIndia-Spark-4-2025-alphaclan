function verifyImage() {
    let fileInput = document.getElementById('imageUpload');
    let formData = new FormData();
    formData.append('image', fileInput.files[0]);

    fetch('/verify', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('result');
        if (data.verified) {
            resultDiv.innerHTML = `<p style='color:green;'>Identity Verified! Distance: ${data.distance.toFixed(2)}</p>`;
        } else {
            resultDiv.innerHTML = `<p style='color:red;'>Verification Failed</p>`;
        }
    })
    .catch(error => console.error('Error:', error));
}
