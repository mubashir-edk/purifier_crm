$(document).ready(function () {

    var productSelect = document.getElementById('formServiceWorkProduct');
    var productSelectLabel = document.getElementById('serviceWorkProductLabel');
    productSelect.innerHTML = '';

    $(productSelectLabel).hide();
    $(productSelect).hide();

    $("#formServiceWorkCustomer").change(function () {

        productSelect.innerHTML = '';

        var selectedCustomer = $('#formServiceWorkCustomer').val();

        console.log(selectedCustomer);

        if (selectedCustomer !== '') {
            
            $(productSelectLabel).show();
            $(productSelect).show();

            $.ajax({
                url: `/view_serviceworks/`,
                type: "GET",
                dataType: "json",
                data: {
                    'selectedCustomer': selectedCustomer,
                },
                success: function (data) {

                    console.log(data.products);

                    var option = document.createElement('option');
                        option.value = '';
                        option.text = '---------';
                        option.selected;
                        productSelect.add(option);

                    data.products.forEach(function (product) {
                        var option = document.createElement('option');
                        option.value = product.id;
                        option.text = product.name + ' (' + product.product_serial + ')';
                        productSelect.add(option);
                    });


                },
                error: function (error) {
                    console.error(error);
                }
            });

        } else {
            $(productSelectLabel).hide();
            $(productSelect).hide();
        }

    });


    var serviceSelect = document.getElementById('formServiceWorkService');
    var serviceSelectLabel = document.getElementById('serviceWorkServiceLabel');

    $(serviceSelectLabel).hide();
    $(serviceSelect).hide();

    $("#formServiceWorkProduct").change(function () {
        var selectedProduct = $('#formServiceWorkProduct').val();

        if (selectedProduct !== '') {
            $(serviceSelectLabel).show();
            $(serviceSelect).show();
            
            // Clear existing checkboxes
            $(serviceSelect).empty();

            $.ajax({
                url: `/view_serviceworks/`,
                type: "GET",
                dataType: "json",
                data: {
                    'selectedProduct': selectedProduct,
                },
                success: function (data) {
                    data.services.forEach(function (service) {
                        var checkbox = $('<input type="checkbox">').attr({
                            id: 'service_' + service.id,
                            value: service.id,
                            name: 'service_name', // Use the same name for all checkboxes
                            class: 'form-checkbox',
                        });
                        var label = $('<label>').attr('for', 'service_' + service.id).addClass('form-label ms-1').text(service.name);

                        $(serviceSelect).append(checkbox).append(label).append('<br>');
                    });
                },
                error: function (error) {
                    console.error(error);
                }
            });
        } else {
            $(serviceSelectLabel).hide();
            $(serviceSelect).hide();
        }
    });

    // SERVICES SELECT CHECK
    document.getElementById('serviceWorkFormG').addEventListener('submit', function(event) {
        var checkboxes = document.querySelectorAll('#formServiceWorkService input[type="checkbox"]');
        var checked = false;
        checkboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                checked = true;
            }
        });
        if (!checked) {
            event.preventDefault();
            alert('Please select at least one service.');
        }
    });


    // DataTable
    var table = $('#serviceworkTable').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": 0 }
        ]
    });

    // Remove sorting icon from the first column header
    $('#serviceworkTable thead th:first-child').removeClass('sorting sorting_asc sorting_desc');

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