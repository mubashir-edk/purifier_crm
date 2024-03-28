const imageInputCategory = document.getElementById('formCategoryImage');
const imagePreviewCategory = document.getElementById('image-preview-category');
const existingImageCategory = document.getElementById('categoryDefaultImage');

imageInputCategory.style.display = 'none';

imageInputCategory.addEventListener('change', function () {
    const file = imageInputCategory.files[0];
    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            imagePreviewCategory.src = e.target.result;
            imagePreviewCategory.style.display = 'block';
            existingImageCategory.style.display = 'none';
        };

        reader.readAsDataURL(file);
    } else {
        imagePreviewCategory.src = '';
        imagePreviewCategory.style.display = 'none';
        existingImageCategory.style.display = 'block';
    }
});