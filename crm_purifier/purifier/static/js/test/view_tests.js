$(document).ready(function () {

    var deleteTestLinks = document.querySelectorAll('.test-delete-icon');

    deleteTestLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var test_id = link.getAttribute('data-testId');
            var test_name = link.getAttribute('data-testName');
            var test_customer = link.getAttribute('data-testCustomer');
            console.log(test_id);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmTestDelete');
            var deleteModalBody = document.getElementById('deleteTestModalBody');
            deleteUrl = `/delete_test/${test_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = "Are you sure, you want to delete <b>" + test_name + "</b> of customer <b>" + test_customer + "</b>?";
        });
    });


    // // DataTable
    // var table = $('#testTable').DataTable({
    //     "columnDefs": [
    //         { "orderable": false, "targets": [0, 8] }
    //     ]
    // });

    // // Remove sorting icon from the first column header
    // $('#testTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');
    // $('#testTable thead th:last-child').removeClass('sorting sorting_asc sorting_desc');

    // // Event listener for DataTable sorting
    // table.on('order.dt', function() {
    //     // Loop through each row in the table
    //     table.rows().every(function(rowIdx, tableLoop, rowLoop) {
    //         // Update the value of forloop.counter for each row
    //         var rowData = this.data();
    //         var cell = this.node().getElementsByTagName('td')[0]; // Assuming forloop.counter is in the first column
    //         cell.innerHTML = rowLoop + 1;
    //     });
    // });

});