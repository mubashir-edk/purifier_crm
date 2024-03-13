const imageInput = document.getElementById('formProductImage');
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
            existingImage.style.display = 'none';
        };

        reader.readAsDataURL(file);
    } else {
        imagePreview.src = '';
        imagePreview.style.display = 'none';
        existingImage.style.display = 'block';
    }
});

$(document).ready(function() {

    $('#productSaveBtn').hide();

    productName = $('#formProductName');
    productSerial = $('#formProductSerial');
    productCategory = $('#formProductCategory');
    productServices = $('#formProductServices');
    categoryReadonly = $('#categoryReadonly');
    servicesReadonly = $('#servicesView');
    imageSelectIcon = $('#imageSelectIcon');

    productName.attr('readonly', 'readonly');
    productSerial.attr('readonly', 'readonly');
    productCategory.hide();
    productServices.hide();
    imageSelectIcon.hide();

    $('#openProductEdit').change(function() {

        if ($(this).prop('checked')) {
            console.log('Checkbox is checked');

            $('#productSaveBtn').show();

            $('#openProductEditLabel').hide();

            $('#productDeleteBtn').hide();

            productName.removeAttr('readonly');
            productSerial.removeAttr('readonly');
            productCategory.show();
            categoryReadonly.hide();
            productServices.show();
            servicesReadonly.hide();
            imageSelectIcon.show();

        } else {
            console.log('Checkbox is unchecked');

        }

    });

    $('#productSaveBtn').click(function() {
        $('#openProductEditLabel').show();
    });

});