$(document).ready(function() {

    // Wait for the page to fully load
    window.addEventListener('load', function() {
        document.getElementById('loadingPage').style.display = 'none';
        
        document.getElementById('navBar').style.display = 'block';
        document.getElementById('mainContent').style.display = 'block';
    });


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
    document.getElementById("mainContent").onscroll = function() {scrollFunction()};

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
    // var hrAndMarkAllReadAppended = false;
    

    // function fetchNotifications() {
    //     $.ajax({
    //         url: '/notifications/',  // URL to fetch notifications
    //         type: "GET",
    //         dataType: "json",
    //         success: function(data) {
    //             console.log(data.notification_data);

    //             var dropdownMenu = $('#notificationDropdownItems');

    //             // Get existing notifications count
    //             var existingCount = dropdownMenu.find('li.custom-item').length;

    //             console.log(data.notifications);

    //             const spanElement = $('<span>').addClass('position-absolute top-0 start-100 translate-middle p-1 bg-danger border border-light rounded-circle');

    //             if (data.notification_data.length > 0) {

    //                 if (!hrAndMarkAllReadAppended) {
    //                     var markAllRead = '<a class="dropdown-item text-center" id="markAllRead" href="/all_notification_read/">Mark all as read</a>';
    //                     var hrLine = '<hr class="m-0 p-0">';
    //                     dropdownMenu.append(markAllRead);
    //                     dropdownMenu.append(hrLine);
    //                     hrAndMarkAllReadAppended = true;
    //                 }

                    
    //                 $('#bellIcon').append(spanElement);

    //                 data.notification_data.forEach(function (notification, index) {

    //                     console.log(notification.message);
    //                     // Only add new notifications
    //                     if (index >= existingCount) {

    //                         if (notification.message_of == "CUSTOMER") {
    //                             var listItem = $('<li class="custom-item d-flex justify-content-between"></li>');
    //                             var anchorTag = '<a class="dropdown-item" href="#">New Customer : ' + notification.message +'</a>';
    //                         } else {
    //                             var listItem = $('<li class="custom-item d-flex justify-content-between"></li>');
    //                             var anchorTag = '<a class="dropdown-item" href="#">Service Work : ' + notification.message +'</a>';
    //                         }
    //                         // var markAsReadAnchorTag = $('<a id="notificationRead" class="dropdown-item text-end w-auto" href="#">Clear</a>');
    //                         listItem.append(anchorTag);
    //                         // listItem.append(markAsReadAnchorTag);
    //                         dropdownMenu.append(listItem);

    //                         if ( notification.once_passed !== true ) {

    //                             $.toast({
    //                                 text: notification.message,
    //                                 heading: notification.message_of == "CUSTOMER" ? 'New Customer' : 'Service Work',
    //                                 icon: notification.message_of == "CUSTOMER" ? 'info' : 'success',
    //                                 showHideTransition: 'fade',
    //                                 allowToastClose: true,
    //                                 hideAfter: 5000,
    //                                 position: 'bottom-right',
    //                                 textAlign: 'left',
    //                                 loader: true,
    //                                 loaderBg: '#9EC600',
    //                             });

    //                             // Trigger AJAX request here
    //                             $.ajax({
    //                                 url: `/update_notification_status/${notification.id}`,
    //                                 type: "POST",
    //                                 data: {},
    //                                 dataType: "json",
    //                                 headers: { "X-CSRFToken": getCookie("csrftoken") },
    //                                 success: function(data) {
    //                                     console.log('AJAX request successful:', data);
    //                                 },
    //                                 error: function(xhr, status, error) {
    //                                     console.error('Error in AJAX request:', error);
    //                                 }
    //                             });

    //                         }
                            
    //                     }

    //                 });

    //             } else {
    //                 spanElement.remove();
    //                 spanText = '<span class="d-flex justify-content-center">No notifications to show.</span>'
    //                 dropdownMenu.empty().append(spanText);
    //             }
    //         }
    //     });
    // }
    // // fetchNotifications();
    // setInterval(fetchNotifications, 5000);

    // $('#markAllRead').click(function() {
    //     fetchNotifications();
    // });


    // frontend.js

    // document.addEventListener('DOMContentLoaded', function () {
    //     const socket = new WebSocket('ws://http://127.0.0.1:8000/ws/notifications/');

    //     socket.onopen = function () {
    //         console.log('WebSocket connection established.');
    //     };

    //     socket.onmessage = function (e) {
    //         const notification = JSON.parse(e.data);
    //         console.log(notification);

    //         // Display toast notification based on the message_of attribute
    //         if (notification.message_of === "CUSTOMER") {
    //             $.toast({
    //                 text: notification.message,
    //                 heading: 'New Customer',
    //                 icon: 'info',
    //                 showHideTransition: 'fade',
    //                 allowToastClose: true,
    //                 hideAfter: 5000,
    //                 position: 'bottom-right',
    //                 textAlign: 'left',
    //                 loader: true,
    //                 loaderBg: '#9EC600',
    //             });
    //         } else if (notification.message_of === "WORK") {
    //             $.toast({
    //                 text: notification.message,
    //                 heading: 'Service Work',
    //                 icon: 'success',
    //                 showHideTransition: 'fade',
    //                 allowToastClose: true,
    //                 hideAfter: 5000,
    //                 position: 'bottom-right',
    //                 textAlign: 'left',
    //                 loader: true,
    //                 loaderBg: '#9EC600',
    //             });
    //         }
    //     };

    //     socket.onclose = function () {
    //         console.log('WebSocket connection closed.');
    //     };
    // });


});