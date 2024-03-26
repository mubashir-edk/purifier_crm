$(document).ready(function() {

    // Wait for the page to fully load
    // window.addEventListener('load', function() {
    //     document.getElementById('loadingPage').style.display = 'none';
        
    //     document.getElementById('navBar').style.display = 'block';
    //     document.getElementById('mainContent').style.display = 'block';
    // });


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


    // main content page sroll up
    // document.getElementById("mainContent").onscroll = function() {scrollFunction()};

    function scrollFunction() {
        if (document.getElementById("mainContent").scrollTop > 200) {
            document.getElementById("scrollToTopBtn").classList.add("show");

        } else {
            document.getElementById("scrollToTopBtn").classList.remove("show");

        }
    }

    $('#scrollToTopBtn').click(function() {
        console.log('Scroll to top');
        var maincontent = document.getElementById("mainContent");
  
        maincontent.scrollTo({
            top: 0,
            behavior: "smooth"
        });
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
    function fetchNotifications() {
        $.ajax({
            url: '/admin_notifications/',
            type: "GET",
            dataType: "json",
            success: function(data) {

                console.log(data);

                $("ul[aria-labelledby='dropdownLeftEndButton']").empty();

                if (data.notification_data.length === 0) {
                    $("ul[aria-labelledby='dropdownNotificationButton']").append(`<li class="cursor-default text-center text-white"><a href="#" class="block text-lg font-base px-4 py-2 cursor-default">No Notifications</a></li>`);
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
    setInterval(fetchNotifications, 10000);

    // mark all notifications read
    $('.mark-all-read').click(function() {
        $.ajax({
            url: '/mark_all_notification_read/',
            type: "GET",
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(xhr, status, error) {
                console.error('Error in AJAX request:', error);
            }
        });
    });

});