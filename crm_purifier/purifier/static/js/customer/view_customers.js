$(document).ready(function() {
    // DataTable
    var table = $('#customersTable').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": 0 }
        ]
    });

    // Remove sorting icon from the first column header
    $('#customersTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');

    // Event listener for DataTable sorting
    table.on('order.dt', function() {
        // Loop through each row in the table
        table.rows().every(function(rowIdx, tableLoop, rowLoop) {
            // Update the value of forloop.counter for each row
            var rowData = this.data();
            var cell = this.node().getElementsByTagName('td')[0]; // Assuming forloop.counter is in the first column
            cell.innerHTML = rowLoop + 1;
        });
    });
});