$(document).ready(function () {

    var create_btn = document.getElementById('createCategoryBtn');

    create_btn.addEventListener('click', function(event) {
        event.preventDefault();

        const imageInputCategory = document.querySelector('#formCategoryImage');
        const imagePreviewCategory = document.querySelector('#image-preview-category');
        const existingImageCategory = document.querySelector('#categoryDefaultImage');

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
    });


    // update modal
    var updateCategoryLinks = document.querySelectorAll('.category-update-icon');

    updateCategoryLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var category_id = link.getAttribute('data-categoryId');
            var category_image = link.getAttribute('data-categoryImage');
            var category_name = link.getAttribute('data-categoryName');
            
            const updateImageInputCategory = document.getElementById('formCategoryImage1');

            const updateImagePreviewCategory = document.getElementById('updateImagePreviewCategory');

            const viewExistingImageCategory = document.getElementById('viewExistImageCategory');

            const viewDefaultImageCategory = document.getElementById('updateCategoryDefaultImage');

            $('#formCategoryName1').val(category_name);
            $('#formCategoryImage1').hide();

            if (category_image) {
                viewExistingImageCategory.src = category_image;
                viewExistingImageCategory.style.display = 'block';
                viewDefaultImageCategory.style.display = 'none';
            } else {
                viewExistingImageCategory.style.display = 'none';
                viewDefaultImageCategory.style.display = 'block';
            }

            console.log(updateImageInputCategory);

            updateImageInputCategory.addEventListener('change', function () {
                const file = updateImageInputCategory.files[0];
                if (file) {
                    const reader = new FileReader();

                    reader.onload = function (e) {
                        updateImagePreviewCategory.src = e.target.result;
                        updateImagePreviewCategory.style.display = 'block';
                        viewExistingImageCategory.style.display = 'none';
                        viewDefaultImageCategory.style.display = 'none';
                    };

                    reader.readAsDataURL(file);
                } else {
                    updateImagePreviewCategory.src = '';
                    updateImagePreviewCategory.style.display = 'none';
                    viewExistingImageCategory.style.display = 'block';
                    viewDefaultImageCategory.style.display = 'block';
                }
            });

            updateUrl = `/update_category/${category_id}`;
            $('#categoryUpdateForm').attr('action', updateUrl)

        });
    });

    // delete modal
    var deleteCategoryLinks = document.querySelectorAll('.category-delete-icon');

    deleteCategoryLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var category_id = link.getAttribute('data-categoryId');
            var category_name = link.getAttribute('data-categoryName');
            console.log(category_id);
            console.log(category_name);

            var confirmDeleteLink = document.getElementById('confirmCategoryDelete');
            var deleteModalBody = document.getElementById('deleteCategoryModalBody');
            deleteUrl = `/delete_category/${category_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = 'You want to delete the category <b>' + category_name + '</b>.';
        });
    });
    
});