const cameraInput = document.getElementById('camera-input');
const photo = document.getElementById('photo');
const fileInput = document.getElementById('file-input');
const resultDiv = document.getElementById('result');

// Function to handle image upload and display
function handleImageUpload(file) {
    const reader = new FileReader();
    reader.onload = function(event) {
        photo.src = event.target.result;
        photo.style.display = 'block';
        uploadImage(event.target.result);  // Call uploadImage with the selected data
    };
    reader.readAsDataURL(file);
}

// Handle capturing image from the camera input
cameraInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        handleImageUpload(file);
    }
});

// Handle uploading image from file input
fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        handleImageUpload(file);
    }
});

// Function to upload image
function uploadImage(data) {
    fetch('/upload', {
        method: 'POST',
        body: JSON.stringify({ image: data }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.error) {
            console.error('Error:', result.error);
            resultDiv.innerText = "Error classifying image.";
        } else {
            resultDiv.innerText = result.result; // Display the classification result
        }
    })
    .catch(error => {
        console.error('Error uploading image:', error);
        resultDiv.innerText = "Error uploading image.";
    });
}
