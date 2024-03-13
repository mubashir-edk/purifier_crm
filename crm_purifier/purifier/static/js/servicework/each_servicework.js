$(document).ready(function () {

    var formSelects = document.getElementById("serviceworkUpdateForm").getElementsByTagName("select");
    var formInputs = document.getElementById("serviceworkUpdateForm").getElementsByTagName("input");
    var formTextareas = document.getElementById("serviceworkUpdateForm").getElementsByTagName("textarea");

    for (var i = 0; i < formSelects.length; i++) {
        formSelects[i].setAttribute("disabled", "true");
    }

    for (var i = 0; i < formInputs.length; i++) {
        formInputs[i].setAttribute("readonly", "true");
    }

    for (var i = 0; i < formTextareas.length; i++) {
        formTextareas[i].setAttribute("readonly", "true");
    }

    $("#productServiceDiv").hide();

    $("#serviceworkSaveBtn").hide();


    var selectedServiceWorkId = $('#serviceWorkId').val();
    var selectedCustomer = $('#formServiceWorkCustomer').val();

    var productSelect = document.getElementById('formServiceWorkProduct');
    var productSelectLabel = document.getElementById('serviceWorkProductLabel');

    var serviceSelect = document.getElementById('formServiceWorkService');
    var serviceSelectLabel = document.getElementById('serviceWorkServiceLabel');

    $(serviceSelectLabel).show();
    $(serviceSelect).show();

    $(productSelectLabel).show();
    $(productSelect).show();


    function productChange() {

        productSelect.innerHTML = '';

        var selectedCustomer = $('#formServiceWorkCustomer').val();

        if (selectedCustomer !== '') {
            
            $(productSelectLabel).show();
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
            $(productSelectLabel).hide();
            $(productSelect).hide();

            $(serviceSelectLabel).hide();
            $(serviceSelect).hide();
        }

    }


    function serviceChange() {

        serviceSelect.innerHTML = '';

        var selectedProduct = $('#formServiceWorkProduct').val();

        if (selectedProduct !== '') {
            
            $(serviceSelectLabel).show();
            $(serviceSelect).show();

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
                            class: 'form-checkbox',
                        });

                        data.default_services.forEach(function (default_service) {
                            if (service.id == default_service.id) {
                                checkbox.prop('checked', true);
                            }
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
    }

    $("#serviceworkEditBtn").click(function (event) {
        event.preventDefault();

        $("#serviceworkEditBtn").hide();
        $("#serviceworkDeleteBtn").hide();
        $("#serviceworkChangeStatus").hide();
        $("#servicesView").hide();
        $("#productServiceDiv").show();
        $("#serviceworkSaveBtn").show();

        for (var i = 0; i < formSelects.length; i++) {
            formSelects[i].removeAttribute("disabled");
        }
    
        for (var i = 0; i < formInputs.length; i++) {
            formInputs[i].removeAttribute("readonly");
        }
    
        for (var i = 0; i < formTextareas.length; i++) {
            formTextareas[i].removeAttribute("readonly");
        }

        serviceChange();

    });


    $("#serviceworkChangeStatus").click(function (event) {
        event.preventDefault();

        $.ajax({
            url: `/servicework_change_status/${selectedServiceWorkId}`,
            type: "GET",
            dataType: "json",
            // data: {
            //     'selectedProduct': selectedProduct,
            // },
            success: function (data) {

                console.log(data);

                // $('.status-of-work ').html(data.html_content);


            },
            error: function (error) {
                console.error(error);
            }
        });

    });


    $("#formServiceWorkCustomer").change(function () {

        serviceSelect.innerHTML = '';
        productChange(); 

    });


    $("#formServiceWorkProduct").change(function () {

        serviceChange();

    });


});