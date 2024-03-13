const imageInput = document.getElementById('formEmployeeProfile');
const imagePreview = document.getElementById('image-preview');
const existingImage = document.querySelector('.col-12.d-flex.justify-content-center img:not(#image-preview)');

imageInput.style.display = 'none';

imageInput.addEventListener('change', function () {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            existingImage.style.display = 'none'; // Hide the existing/default image
        };

        reader.readAsDataURL(file);
    } else {
        imagePreview.src = '';
        imagePreview.style.display = 'none';
        existingImage.style.display = 'block'; // Show the existing/default image
    }
});
