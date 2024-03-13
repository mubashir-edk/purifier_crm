$(document).ready(function (e) {

    // Assign
    var assignServiceWorkLinks = document.querySelectorAll('#assignWorkBtn');

    assignServiceWorkLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var servicework_id = link.getAttribute('data-bs-servicework');
            console.log("asdasd: " + servicework_id);

            // Set the href attribute of the "Delete" link
            var confirmAssignLink = document.getElementById('confirmWorkAssign');
            assignUrl = `/assign_servicer/${servicework_id}`;

            confirmAssignLink.setAttribute('action', assignUrl);
        });
    });


    // UnAssign
    var unAssignServiceWorkLinks = document.querySelectorAll('#confirmWorkUnAssign');

    unAssignServiceWorkLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var serviceworkId = link.getAttribute('data-bs-service');
            var servicework_service = link.getAttribute('data-bs-serviceName');
            var servicework_servicer = link.getAttribute('data-bs-servicer');

            console.log(serviceworkId);
            console.log(servicework_service);
            console.log(servicework_servicer);

            // Set the href attribute of the "Delete" link
            var confirmUnAssignLink = document.getElementById('confirmUnAssign');
            var unAssignModalBody = document.getElementById('unAssignModalBody');
            unAssignUrl = `/unassign_servicer/${serviceworkId}`;

            confirmUnAssignLink.href = unAssignUrl;
            console.log(confirmUnAssignLink);
            unAssignModalBody.innerHTML = 'you want to unAssign <b>' + servicework_servicer + '</b> from <b>' + servicework_service + '</b>.';
        });
    });


    // DataTable
    var table = $('#serviceAssignTable').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": 0 }
        ]
    });

    // Remove sorting icon from the first column header
    $('#serviceAssignTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');

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