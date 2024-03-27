$(document).ready(function() {

    // sidenav toggle
    var isViewModify = localStorage.getItem('isViewModify') === 'true';
    
    var pageBody = $('#pageBodyView');
    if (window.innerWidth > 768) {
        if (isViewModify) {
            pageBody.addClass('view-modify');
        } else {
            pageBody.removeClass('view-modify');
        }
    }

    $('#sideNavBoolean').prop('checked', isViewModify);

    $('#sideNavBoolean').change(function() {
        var isChecked = $(this).prop('checked');
        console.log('Checkbox state changed:', isChecked);

        localStorage.setItem('isViewModify', isChecked);

        if (window.innerWidth > 768) {
            if (isChecked) {
                pageBody.addClass('view-modify');
            } else {
                pageBody.removeClass('view-modify');
            }
        }
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // notification
    let noNotificationsShown = false;

    function fetchNotifications() {
        $.ajax({
            url: '/admin_notifications/',
            type: "GET",
            dataType: "json",
            success: function(data) {

                console.log(data);

                const notificationList = $("ul[aria-labelledby='dropdownNotificationButton']");

                if (data.notification_data.length === 0) {
                    if (!noNotificationsShown) {
                        notificationList.append(`<li class="cursor-default text-center text-white"><a href="#" class="block text-lg font-base px-4 py-2 cursor-default">No Notifications</a></li>`);
                        noNotificationsShown = true;
                    }
                } else {
                    notificationList.empty(); // Empty the list before adding new notifications
                    noNotificationsShown = false; // Reset the flag if there are notifications
                }

                data.notification_data.forEach(function (notification) {

                    if (!notification.once_passed) {

                        if (notification.message_of == "SERVICE_WORK_COMPLETED") {
                            $.toast({
                                text: notification.message,
                                heading: 'Service Work',
                                showHideTransition: 'plain',
                                hideAfter: 5000,
                                position: 'bottom-right', 
                            })
                        }

                        if (notification.message_of == "NEW_CUSTOMER") {
                            $.toast({
                                text: notification.message,
                                heading: 'New Customer',
                                showHideTransition: 'plain',
                                hideAfter: 5000,
                                position: 'bottom-right', 
                            })
                        }

                        $.ajax({
                            url: `/update_notification_status/${notification.id}`,
                            type: "POST",
                            data: {},
                            dataType: "json",
                            headers: { "X-CSRFToken": getCookie("csrftoken") },
                            success: function(data) {
                                console.log('AJAX request successful:', data);
                            },
                            error: function(xhr, status, error) {
                                console.error('Error in AJAX request:', error);
                            }
                        });
                    } else {
                        console.log("Once toast appeared");
                    }

                    $("ul[aria-labelledby='dropdownNotificationButton']").append(`<li class="cursor-default"><a href="#" class="block text-lg font-base px-4 py-2 rounded-lg bg-white shadow hover:bg-gray-500 hover:text-white cursor-default">${notification.message}</a></li>`);

                });
            },
            error: function(xhr, status, error) {
                console.error('Error in AJAX request:', error);
            }
        });
    }

    fetchNotifications();
    setInterval(fetchNotifications, 100);

    // mark all notifications read
    $('.mark-all-read').click(function() {
        $.ajax({
            url: '/mark_all_notification_read/',
            type: "GET",
            dataType: "json",
            success: function(data) {
                console.log(data);
                $("ul[aria-labelledby='dropdownNotificationButton']").empty();
            },
            error: function(xhr, status, error) {
                console.error('Error in AJAX request:', error);
            }
        });
    });

});