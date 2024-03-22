const imageInput = document.getElementById('formCustomerProfile');
const imagePreview = document.getElementById('image-preview');
const existingImage = document.querySelector('.default-image');

imageInput.style.display = 'none';

imageInput.addEventListener('change', function () {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            existingImage.style.display = 'none';
        };

        reader.readAsDataURL(file);
    } else {
        imagePreview.src = '';
        imagePreview.style.display = 'none';
        existingImage.style.display = 'block';
    }
});

$('#formCustomerInstalledProduct div').find('label').addClass('flex items-center gap-x-1');