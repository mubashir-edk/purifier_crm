$(document).ready(function () {

    // filtering servicers not existing
    var employeeSelector = $('#formServicerName');
    var serviceNameLabel = $('#serviceNameLabel');

    // employeeSelector.focus(function () {
    $('#createServicerModal').on('show.bs.modal', function () {
        employeeSelector.empty();

        $.ajax({
            url: `/fetch_employee_filtered/`,
            type: "GET",
            dataType: "json",
            success: function (data) {

                console.log(data.employees);
                console.log(data);

                if (data.employees_exists) {

                    // Add default option
                    employeeSelector.append($('<option>', {
                        value: '',
                        text: '---------',
                        selected: true
                    }));

                    // Add employees to the dropdown
                    data.employees.forEach(function (employee) {
                        employeeSelector.append($('<option>', {
                            value: employee.id,
                            text: employee.name
                        }));
                    });

                } else {

                    employeeSelector.hide();
                    serviceNameLabel.hide();

                    var createServicerModalTitle = document.getElementById('createServicerModalTitle');

                    createServicerModalTitle.innerHTML = 'No employees to add.';
                    $('#createModalBody').hide();
                    $('#createModalFooter').hide();

                }


            },
            error: function (error) {
                console.error(error);
            }
        });

    });


    // fetching employee data
    var employeeDetails = $("#servicerDetails");
    var employeeCode = $("#employeeCode");
    var employeeContact = $("#employeeContact");

    employeeDetails.hide();

    $("#formServicerName").change(function () {

        var selectedValue = $(this).val();

        console.log(selectedValue);

        $.ajax({
            url: `/fetch_servicer/${selectedValue}`,
            type: "GET",
            dataType: "json",
            success: function (data) {
                employeeDetails.show();
                employeeCode.val(data.employee.employee_code);
                employeeContact.val(data.employee.mobile);
            },
            error: function (error) {
                console.error(error);
            }
        });

    });


    // delete link
    var deleteServicerLinks = document.querySelectorAll('.delete-servicer-btn');

    deleteServicerLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var servicer_id = link.getAttribute('data-bs-servicerId');
            var servicer_code = link.getAttribute('data-bs-servicerCode');
            console.log(servicer_id);
            console.log(servicer_code);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmServicerDelete');
            var deleteModalBody = document.getElementById('deleteServicerModalBody');
            deleteUrl = `/delete_servicer/${servicer_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = 'you want to remove <b>' + servicer_code + '</b> from servicer.';
        });
    });


    // DataTable
    var table = $('#servicersTable').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": [0, 4]},
        ]
    });

    // Remove sorting icon from the first column header
    $('#servicersTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');
    $('#servicersTable thead th:last-child').removeClass('sorting sorting_asc sorting_desc');

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