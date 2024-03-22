const imageInput = document.getElementById('formProductImage');
const imagePreview = document.getElementById('image-preview');
const existImage = document.getElementById('product-image');

imageInput.style.display = 'none';

imageInput.addEventListener('change', function () {
    const file = imageInput.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block';
            existImage.style.display = 'none';
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
    categoryReadonly = $('#categoryReadonly');
    imageSelectIcon = $('#imageSelectIcon');

    productName.attr('readonly', 'readonly');
    productSerial.attr('readonly', 'readonly');
    productCategory.hide();
    imageSelectIcon.hide();

    productServiceDiv = $('#productServiceDiv');
    servicesReadonly = $('#servicesView');

    productServiceDiv.hide();

    $('#openProductEdit').change(function() {

        if ($(this).prop('checked')) {
            console.log('Checkbox is checked');

            $('#productSaveBtn').show();
            $('#openProductEditBtn').hide();
            $('#productDeleteBtn').hide();

            productName.removeAttr('readonly');
            productSerial.removeAttr('readonly');
            productCategory.show();
            categoryReadonly.hide();
            imageSelectIcon.show();

            productServiceDiv.show();
            servicesReadonly.hide();

            $('#formProductServices div').find('label').addClass('flex items-center ms-1');
            $('#formProductServices div label').find('input').addClass('me-1');

        } else {
            console.log('Checkbox is unchecked');
        }

    });

    $('#productSaveBtn').click(function() {
        $('#openProductEditBtn').show();
    });

});