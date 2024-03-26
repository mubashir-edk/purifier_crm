$(document).ready(function () {

    var deleteTestLinks = document.querySelectorAll('.test-delete-icon');

    deleteTestLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            var test_id = link.getAttribute('data-testId');
            var test_name = link.getAttribute('data-testName');
            var test_customer = link.getAttribute('data-testCustomer');
            console.log(test_id);

            // Set the href attribute of the "Delete" link
            var confirmDeleteLink = document.getElementById('confirmTestDelete');
            var deleteModalBody = document.getElementById('deleteTestModalBody');
            deleteUrl = `/delete_test/${test_id}`;

            confirmDeleteLink.href = deleteUrl;
            deleteModalBody.innerHTML = "Are you sure, you want to delete <b>" + test_name + "</b> of customer <b>" + test_customer + "</b>?";
        });
    });


    // Sort direction
    var sortDirection = {};

    // Function to sort table data
    function sortTable(column, order) {
        var $tbody = $('#tests_table tbody');
        var rows = $tbody.find('tr').toArray();

        // Sort the rows
        rows.sort(function (a, b) {
            // Skip sorting for the first column
            if (column === 0) return 0;

            var valA = $(a).find('th').eq(column).text().trim();
            var valB = $(b).find('th').eq(column).text().trim();

            if (valA < valB) return order === 'asc' ? -1 : 1;
            if (valA > valB) return order === 'asc' ? 1 : -1;
            return 0;
        });

        // Append sorted rows to table
        $tbody.empty().append(rows);
    }

    // Click event handler for table headers (excluding the first one)
    $('#tests_table').on('click', 'th:not(:first)', function () {
        var columnIndex = $(this).index();
        var columnName = $(this).text().trim().toLowerCase();
        var order = sortDirection[columnName] === 'asc' ? 'desc' : 'asc';

        // Remove sorting indicators from other columns
        $('#tests_table th').removeClass('sorted-asc sorted-desc');

        // Set sorting indicator for the clicked column
        $(this).addClass(order === 'asc' ? 'sorted-asc' : 'sorted-desc');

        // Sort the table
        sortTable(columnIndex, order);

        // Update sort direction
        sortDirection[columnName] = order;
    });

    // Search functionality
    $('#searchInput').on('keyup', function() {
        var searchText = $(this).val().toLowerCase();
        var totalRows = $('#tests_table tbody tr').length;
        
        if (searchText === '') {
            // If search input is empty, re-run pagination
            var entries = parseInt($('#showEntriesSelect').val());
            var totalPages = Math.ceil(totalRows / entries);
            var currentPage = 1;
            
            showPage(currentPage, entries);
            generatePaginationButtons(totalPages, currentPage);
        } else {
            $('#tests_table tbody tr').filter(function() {
                $(this).toggle($(this).text().toLowerCase().indexOf(searchText) > -1);
            });
        }
    });

    var rowsPerPage = parseInt($('#showEntriesSelect').val()); // Default rows per page
    var totalRows = $('#tests_table tbody tr').length;
    var totalPages = Math.ceil(totalRows / rowsPerPage);
    var currentPage = 1;
    var maxPaginationButtons = 7;

    function showPage(page, entries) {
        var start = (page - 1) * entries;
        var end = start + entries;

        $('#tests_table tbody tr').hide();
        $('#tests_table tbody tr').slice(start, end).show();
    }

    function generatePaginationButtons(totalPages, currentPage) {
        $('#pagination').empty();

        var startPage = Math.max(1, currentPage - Math.floor(maxPaginationButtons / 2));
        var endPage = Math.min(totalPages, startPage + maxPaginationButtons - 1);

        if (endPage - startPage + 1 < maxPaginationButtons) {
            startPage = Math.max(1, endPage - maxPaginationButtons + 1);
        }

        $('#pagination').append('<button class="paginationButton dark:bg-gray-800 text-white font-bold px-3 py-2 rounded mr-2 hover:bg-blue-700" data-page="1">&lt;&lt;</button>');

        if (currentPage > 1) {
            $('#pagination').append('<button class="paginationButton dark:bg-gray-800 text-white font-bold px-4 py-2 rounded mr-2 hover:bg-blue-700" data-page="' + (currentPage - 1) + '">&lt;</button>');
        }

        for (var i = startPage; i <= endPage; i++) {
            var activeClass = i === currentPage ? 'bg-red-500' : '';
            $('#pagination').append('<button class="paginationButton ' + activeClass + ' text-black font-medium hover:text-white px-4 py-2 rounded-full mr-2 hover:bg-blue-700" data-page="' + i + '">' + i + '</button>');
        }

        if (currentPage < totalPages) {
            $('#pagination').append('<button class="paginationButton dark:bg-gray-800 text-white font-bold px-4 py-2 rounded mr-2 hover:bg-blue-700" data-page="' + (currentPage + 1) + '">&gt;</button>');
        }

        $('#pagination').append('<button class="paginationButton dark:bg-gray-800 text-white font-bold px-3 py-2 rounded mr-2 hover:bg-blue-700" data-page="' + totalPages + '">&gt;&gt;</button>');
    }

    showPage(currentPage, rowsPerPage);
    generatePaginationButtons(totalPages, currentPage);

    $(document).on('click', '.paginationButton', function() {
        currentPage = parseInt($(this).attr('data-page'));
        showPage(currentPage, rowsPerPage);
        generatePaginationButtons(totalPages, currentPage);
    });

    $('#showEntriesSelect').on('change', function() {
        rowsPerPage = parseInt($(this).val());
        totalPages = Math.ceil(totalRows / rowsPerPage);
        currentPage = 1;
        showPage(currentPage, rowsPerPage);
        generatePaginationButtons(totalPages, currentPage);
    });

});