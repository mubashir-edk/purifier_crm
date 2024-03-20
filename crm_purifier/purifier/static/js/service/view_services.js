$(document).ready(function () {

    var deleteServiceLinks = document.querySelectorAll('.service-delete-icon');

    console.log(deleteServiceLinks);

    deleteServiceLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var service_id = link.getAttribute('data-serviceId');
            var service_name = link.getAttribute('data-serviceName');
            console.log(service_id);
            console.log(service_name);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmServiceDelete');
            var deleteModalBody = document.getElementById('deleteServiceModalBody');
            deleteUrl = `/delete_service/${service_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = "Are you sure you want to delete this customer <b>" + service_name + "</b>? This customer user access will loss and can't retrieve it later."
        });
    });


    var updateServiceLinks = document.querySelectorAll('.service-update-icon');

    updateServiceLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var service_id = link.getAttribute('data-serviceId');
            var service_name = link.getAttribute('data-serviceName');
            console.log(service_id);
            console.log(service_name);
            
            $('#serviceUpdateForm #formServiceName').attr('value', service_name);
            console.log($('#formServiceName'));

            // Set the href attribute of the "Update" link
            // var confirmServiceLink = document.getElementById('updateServiceBtn');

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