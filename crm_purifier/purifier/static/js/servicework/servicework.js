$(document).ready(function () {

    var productSelect = document.getElementById('formServiceWorkProduct');

    $("#formServiceWorkProduct").prop("disabled", true);

    $("#formServiceWorkCustomer").change(function () {

        productSelect.innerHTML = '';

        var selectedCustomer = $('#formServiceWorkCustomer').val();

        console.log(selectedCustomer);

        if (selectedCustomer !== '') {

            $("#formServiceWorkProduct").prop("disabled", false);

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
            $("#formServiceWorkProduct").prop("disabled", true);
            var defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.text = '---------';
            productSelect.appendChild(defaultOption);
        }

    });


    var serviceSelect = document.getElementById('formServiceWorkService');

    $(serviceSelect).hide();

    $("#formServiceWorkProduct").change(function () {
        var selectedProduct = $('#formServiceWorkProduct').val();

        if (selectedProduct !== '') {
            // $(serviceSelectLabel).show();
            $(serviceSelect).show();
            $('#toShowServices').hide();
            
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
                            class: 'w-4 h-4 text-black border-gray-300 rounded ms-2',
                        });
                        var label = $('<label>').attr('for', 'service_' + service.id).text(service.name);

                        container = $('<div>').addClass('flex items-center gap-x-1');

                        container.append(checkbox).append(label);

                        $(serviceSelect).append(container);
                    });
                },
                error: function (error) {
                    console.error(error);
                }
            });
        } else {
            $(serviceSelect).hide();
            $('#toShowServices').show();
        }
    });

    // SERVICES SELECT CHECK
    // document.getElementById('serviceWorkFormG').addEventListener('submit', function(event) {
    //     var checkboxes = document.querySelectorAll('#formServiceWorkService input[type="checkbox"]');
    //     var checked = false;
    //     checkboxes.forEach(function(checkbox) {
    //         if (checkbox.checked) {
    //             checked = true;
    //         }
    //     });
    //     if (!checked) {
    //         event.preventDefault();
    //         alert('Please select at least one service.');
    //     }
    // });

});