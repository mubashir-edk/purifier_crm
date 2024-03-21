const imageInputProduct = document.getElementById('formProductImage');
const imagePreviewProduct = document.getElementById('image-preview-product');
const defaultProductImage = document.getElementById('productDefaultImgae');

imageInputProduct.style.display = 'none';

imageInputProduct.addEventListener('change', function () {
    const file = imageInputProduct.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreviewProduct.src = e.target.result;
            defaultProductImage.style.display = 'none';
            imagePreviewProduct.style.display = 'block';
        };

        reader.readAsDataURL(file);
    } else {
        imagePreviewProduct.src = '';
        imagePreviewProduct.style.display = 'none';
        defaultProductImage.style.display = 'block';
    }
});

$(document).ready(function() {
    $('#formProductServices div').find('label').addClass('flex items-center ms-1');
    $('#formProductServices div label').find('input').addClass('me-1');
});