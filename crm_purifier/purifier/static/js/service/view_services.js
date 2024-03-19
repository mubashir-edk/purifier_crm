$(document).ready(function () {

    var deleteServiceLinks = document.querySelectorAll('.delete-service-btn');

    deleteServiceLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var service_id = link.getAttribute('data-bs-serviceId');
            var service_name = link.getAttribute('data-bs-serviceName');
            console.log(service_id);
            console.log(service_name);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmServiceDelete');
            var deleteModalBody = document.getElementById('deleteServiceModalBody');
            deleteUrl = `/delete_service/${service_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = 'you want to delete <b>' + service_name + '</b> from services list.';
        });
    });


    var updateServiceLinks = document.querySelectorAll('.update-service-btn');

    updateServiceLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var service_id = link.getAttribute('data-bs-serviceId');
            var service_name = link.getAttribute('data-bs-serviceName');
            console.log(service_id);
            console.log(service_name);
            
            $('#serviceUpdateForm #formServiceName').attr('value', service_name);
            console.log($('#formServiceName'));

            // Set the href attribute of the "Update" link
            var confirmServiceLink = document.getElementById('updateServiceBtn');

            updateUrl = `/update_service/${service_id}`;
            $('#serviceUpdateForm').attr('action', updateUrl)

            console.log($('#serviceUpdateForm'));

        });
    });


    // DataTable
    // var table = $('#servicesTable').DataTable({
    //     "columnDefs": [
    //         { "orderable": false, "targets": 0 }
    //     ]
    // });

    // // Remove sorting icon from the first column header
    // $('#servicesTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');

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