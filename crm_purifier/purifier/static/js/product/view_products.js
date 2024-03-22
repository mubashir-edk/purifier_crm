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

// $(document).ready(function() {
//     // DataTable
//     var table = $('#productsTable').DataTable({
//         "columnDefs": [
//             { "orderable": false, "targets": 0 }
//         ]
//     });

//     // Remove sorting icon from the first column header
//     $('#productsTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');

//     // Event listener for DataTable sorting
//     table.on('order.dt', function() {
//         // Loop through each row in the table
//         table.rows().every(function(rowIdx, tableLoop, rowLoop) {
//             // Update the value of forloop.counter for each row
//             var rowData = this.data();
//             var cell = this.node().getElementsByTagName('td')[0]; // Assuming forloop.counter is in the first column
//             cell.innerHTML = rowLoop + 1;
//         });
//     });
// });


