$(document).ready(function () {

    $("#formServiceWorkCustomer").prop("disabled", true);
    $("#formServiceWorkProduct").prop("disabled", true);
    
    $('#formServiceWorkDate').hide();

    $("#productServiceDiv").hide();
    $("#serviceworkSaveBtn").hide();


    var selectedServiceWorkId = $('#serviceWorkId').val();
    var selectedCustomer = $('#formServiceWorkCustomer').val();

    var productSelect = document.getElementById('formServiceWorkProduct');
    var serviceSelect = document.getElementById('formServiceWorkService');

    $(serviceSelect).show();
    $(productSelect).show();
    $('#toShowServices').hide();


    function productChange() {

        productSelect.innerHTML = '';

        var selectedCustomer = $('#formServiceWorkCustomer').val();

        if (selectedCustomer !== '') {
            
            $(productSelect).show();

            $.ajax({
                url: `/each_service_work/${selectedServiceWorkId}`,
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
                        option.selected = true;
                        productSelect.add(option);

                    data.products.forEach(function (product) {
                        var option = document.createElement('option');
                        option.value = product.id;
                        option.text = product.name;
                        productSelect.add(option);
                    });


                },
                error: function (error) {
                    console.error(error);
                }
            });

        } else {
            $("#formServiceWorkProduct").prop("disabled", true);
            var option = document.createElement('option');
                        option.value = '';
                        option.text = '---------';
                        option.selected;
                        productSelect.add(option);
        }

    }


    function serviceChange() {

        serviceSelect.innerHTML = '';

        var selectedProduct = $('#formServiceWorkProduct').val();

        if (selectedProduct !== '') {
            
            $(serviceSelect).show();
            $('#toShowServices').hide();

            $.ajax({
                url: `/each_service_work/${selectedServiceWorkId}`,
                type: "GET",
                dataType: "json",
                data: {
                    'selectedProduct': selectedProduct,
                },
                success: function (data) {

                    console.log(data.services);

                    data.services.forEach(function (service) {
                        var checkbox = $('<input type="checkbox">').attr({
                            id: 'service_' + service.id,
                            value: service.id,
                            name: 'service_name', // Use the same name for all checkboxes
                            class: 'w-4 h-4 text-black border-gray-300 rounded ms-2',
                        });

                        data.default_services.forEach(function (default_service) {
                            if (service.id == default_service.id) {
                                checkbox.prop('checked', true);
                            }
                        });


                        var label = $('<label>').attr('for', 'service_' + service.id).addClass('form-label ms-1').text(service.name);

                        container = $('<div>').addClass('flex items-center gap-x-1');

                        container.append(checkbox).append(label);

                        $(serviceSelect).append(container);

                        $('#productServiceDiv').addClass('overflow-y-auto h-28');

                    });


                },
                error: function (error) {
                    console.error(error);
                }
            });

        } else {
            $(serviceSelect).hide();
            $('#toShowServices').show();
            $('#productServiceDiv').addClass('overflow-none h-auto');
        }
    }

    $("#serviceworkEditBtn").click(function (event) {
        event.preventDefault();

        $("#serviceworkEditBtn").hide();
        $("#serviceworkDeleteBtn").hide();
        $("#serviceworkChangeStatus").hide();
        $("#servicesView").hide();
        $("#productServiceDiv").show();
        $("#serviceworkSaveBtn").show();

        $("#formServiceWorkCustomer").prop("disabled", false);
        $("#formServiceWorkProduct").prop("disabled", false);

        $('#dateReadonly').hide();
        $('#formServiceWorkDate').show();

        serviceChange();
    });

    $("#formServiceWorkCustomer").change(function () {
        serviceSelect.innerHTML = '';
        $("#formServiceWorkProduct").prop("disabled", false);
        productChange();
    });


    $("#formServiceWorkProduct").change(function () {
        serviceChange();
    });

});