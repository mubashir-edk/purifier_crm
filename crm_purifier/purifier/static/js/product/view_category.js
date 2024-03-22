$(document).ready(function () {

    var create_btn = document.getElementById('createCategoryBtn');

    create_btn.addEventListener('click', function(event) {
        event.preventDefault();

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
    });


    // update modal
    var updateCategoryLinks = document.querySelectorAll('.category-update-icon');

    updateCategoryLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var category_id = link.getAttribute('data-categoryId');
            var category_image = link.getAttribute('data-categoryImage');
            var category_name = link.getAttribute('data-categoryName');

            console.log(category_image)
            
            const updateImageInputCategory = document.querySelector('#formCategoryImage');
            const updateImagePreviewCategory = document.querySelector('.updateImagePreviewCategory');
            const viewExistingImageCategory = document.querySelector('.viewExistImageCategory');
            const viewDefaultImageCategory = document.querySelector('.updateCategoryDefaultImage');

            $('#categoryUpdateForm #formCategoryName').val(category_name);
            updateImageInputCategory.style.display = 'none';
            // $('#categoryUpdateForm #formCategoryImage').hide();

            $(viewExistingImageCategory).attr('src', category_image);

            if (category_image) {
                viewDefaultImageCategory.style.display = 'none';
            } else {
                viewExistingImageCategory.style.display = 'none';
            }

            // updateImageInputCategory.addEventListener('change', function () {
            //     const file = updateImageInputCategory.files[0];
            //     if (file) {
            //         console.log("there is already a file");
            //         const reader = new FileReader();

            //         reader.onload = function (e) {
            //             // updateImagePreviewCategory.src = e.target.result;
            //             $(updateImagePreviewCategory).attr('src', e.target.result);
            //             $(updateImagePreviewCategory).show();
            //             $(viewExistingImageCategory).hide();
            //             $(viewDefaultImageCategory).hide();
            //         };

            //         reader.readAsDataURL(file);
            //     } else {
            //         // updateImagePreviewCategory.src = '';
            //         $(updateImagePreviewCategory).attr('src', '');
            //         $(updateImagePreviewCategory).hide();
            //         $(viewExistingImageCategory).show();
            //         $(viewDefaultImageCategory).show();
            //     }
            // });

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