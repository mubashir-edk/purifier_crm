$(document).ready(function () {

    // filtering servicers not existing
    var employeeSelector = $('#formServicerName');
    var serviceNameLabel = $('#serviceNameLabel');
    var serviceCode = $("#servicerCode");
    var serviceMobile = $("#servicerMobile");

    $('#bodyNoEmployee').hide();

    $('#add-servicer-modal').click(function () {
        employeeSelector.empty();
        serviceCode.hide();
        serviceMobile.hide();

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

                    $('#bodyIfEmployee').hide();
                    $('#bodyNoEmployee').show();

                }


            },
            error: function (error) {
                console.error(error);
            }
        });

    });

    $('#ifNoServicer').click(function () {
        employeeSelector.empty();
        serviceCode.hide();
        serviceMobile.hide();

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

                    $('#bodyIfEmployee').hide();
                    $('#bodyNoEmployee').show();

                }


            },
            error: function (error) {
                console.error(error);
            }
        });

    });


    // fetching employee data
    var employeeCode = $("#employeeCode");
    var employeeContact = $("#employeeContact");

    serviceCode.hide();
    serviceMobile.hide();

    $("#formServicerName").change(function () {

        var selectedValue = $(this).val();

        if (!selectedValue) {
            serviceCode.hide();
            serviceMobile.hide();
        } else {
            serviceCode.show();
            serviceMobile.show();
        }

        console.log(selectedValue);

        $.ajax({
            url: `/fetch_servicer/${selectedValue}`,
            type: "GET",
            dataType: "json",
            success: function (data) {
                employeeCode.val(data.employee.employee_code);
                console.log(employeeCode.val())
                employeeContact.val(data.employee.mobile);
            },
            error: function (error) {
                console.error(error);
            }
        });

    });


    // delete link
    var deleteServicerLinks = document.querySelectorAll('.servicer-delete-icon');

    deleteServicerLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var servicer_id = link.getAttribute('data-servicerId');
            var servicer_code = link.getAttribute('data-servicerCode');
            console.log(servicer_id);
            console.log(servicer_code);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmServicerDelete');
            var deleteModalBody = document.getElementById('deleteServicerModalBody');
            deleteUrl = `/delete_servicer/${servicer_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = "Are you sure you want to remove this employee <b>" + servicer_code + "</b> from servicer?";
        });
    });


    // // DataTable
    // var table = $('#servicersTable').DataTable({
    //     "columnDefs": [
    //         { "orderable": false, "targets": [0, 4]},
    //     ]
    // });

    // // Remove sorting icon from the first column header
    // $('#servicersTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');
    // $('#servicersTable thead th:last-child').removeClass('sorting sorting_asc sorting_desc');

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