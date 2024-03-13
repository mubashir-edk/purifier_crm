$(document).ready(function () {

    // update modal
    var updateCategoryLinks = document.querySelectorAll('.update-category-btn');

    updateCategoryLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            // Prevent the default behavior of the link
            event.preventDefault();

            // Get the 'data-bs-id' and 'data-bs-name' and 'data-bs-chalan' attributes for the clicked link
            var category_id = link.getAttribute('data-bs-category');
            var category_image = link.getAttribute('data-bs-categoryImage');
            var categoryname = link.getAttribute('data-bs-categoryname');
            // var categoryNameInput = document.getElementById('formCategoryName');
            console.log(category_id);
            console.log(category_image);
            console.log(categoryname);
            
            const updateImageInputCategory = document.getElementById('formCategoryImage');
            const updateImagePreviewCategory = document.getElementById('update-image-preview-category');
            const updateExistingImageCategory = document.getElementById('updateCategoryDefaultImage');
            const viewExistingImageCategory = document.getElementById('view-exist-image-category');

            updateImageInputCategory.style.display = 'none';

            if (category_image) {
                updateExistingImageCategory.style.display = 'none';
            } else {
                viewExistingImageCategory.style.display = 'none';
            }

            updateImageInputCategory.addEventListener('change', function () {
                const file = updateImageInputCategory.files[0];
                if (file) {
                    const reader = new FileReader();

                    reader.onload = function (e) {
                        updateImagePreviewCategory.src = e.target.result;
                        updateImagePreviewCategory.style.display = 'block';
                        viewExistingImageCategory.style.display = 'none';
                        updateExistingImageCategory.style.display = 'none'; // Hide the existing/default image
                    };

                    reader.readAsDataURL(file);
                } else {
                    updateImagePreviewCategory.src = '';
                    updateImagePreviewCategory.style.display = 'none';
                    viewExistingImageCategory.style.display = 'block';
                    updateExistingImageCategory.style.display = 'block'; // Show the existing/default image
                }
            });


            $('#view-exist-image-category').attr('src', category_image);
            $('#formCategoryName').val(categoryname);

            updateUrl = `/update_category/${category_id}`;
            $('#categoryUpdateForm').attr('action', updateUrl)

        });
    });


    // delete modal
    var deleteCategoryLinks = document.querySelectorAll('.delete-category-btn');

    deleteCategoryLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var category_id = link.getAttribute('data-bs-category');
            var category_name = link.getAttribute('data-bs-categoryName');
            console.log(category_id);
            console.log(category_name);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmCategoryDelete');
            var deleteModalBody = document.getElementById('deleteCategoryModalBody');
            deleteUrl = `/delete_category/${category_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = 'You want to delete the category <b>' + category_name + '</b>.';
        });
    });

    // show products of each category modal
    var categoryProductsLinks = document.querySelectorAll('.category-products');

    categoryProductsLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
    
            // Define categoryId and categoryProductsUrl in the current scope
            const categoryId = link.getAttribute('data-bs-categoryId');
            console.log(categoryId);
    
            // Set the href attribute of the "Delete" link
            const categoryProductsUrl = `/view_category_products/${categoryId}`;
            console.log(categoryProductsUrl);
    
            // Make the AJAX call
            $.ajax({
                url: categoryProductsUrl,
                type: "GET",
                dataType: "json",
                data: {
                    'categoryId': categoryId,
                },
                success: function (data) {
                    console.log(data.category_products);
                    console.log(data.category.name);

                    $('#categoryProductsModalTitle').text( data.category.name + ' category products');
                        console.log($('#categoryProductsModalTitle'));
                    
                    if (data.category_products_exists) {
                        var table = $('<table>').addClass('table table-bordered align-middle');
                        var thead = $('<thead>').addClass('text-white').append($('<tr>').append($('<th>'), $('<th>').text('Product Serial'), $('<th>').text('Product Name')));
                        var tbody = $('<tbody>').addClass('bg-white');
                        
                        data.category_products.forEach(function (category_product, index) {
                            var tr = $('<tr>').append($('<td>').text(index + 1), $('<td>').text(category_product.product_serial), $('<td>').text(category_product.name));
                            tbody.append(tr);
                        });
                
                        table.append(thead, tbody);
                        $('#categoryProductsModalBody').empty().append(table);
                    } else {
                        $('#categoryProductsModalBody').empty().addClass('text-center').text('No products for this category.');
                    }

                },
                error: function (error) {
                    console.error(error);
                    console.log(categoryProductsUrl);
                }
            });
        });
    });
    
    
});