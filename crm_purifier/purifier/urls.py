from django.urls import path
from . import views

app_name = 'purifier'

urlpatterns = [
    
    # Employee
    path('view_employees/', views.viewEmployees, name='view_employees'),
    path('create_employee/', views.createEmployee, name='create_employee'),
    path('each_employee/<uuid:id>', views.eachEmployee, name='each_employee'),
    path('update_employee/<uuid:id>', views.updateEmployee, name='update_employee'),
    path('delete_employee/<uuid:id>', views.deleteEmployee, name='delete_employee'),
    
    # Customer
    path('view_customers/', views.viewCustomers, name='view_customers'),
    path('create_customer/', views.createCustomer, name='create_customer'),
    path('each_customer/<uuid:id>', views.eachCustomer, name='each_customer'),
    path('update_customer/<uuid:id>', views.updateCustomer, name='update_customer'),
    path('delete_customer/<uuid:id>', views.deleteCustomer, name='delete_customer'),
    
    # Product
    path('view_categories/', views.viewCategories, name='view_categories'),
    path('create_category/', views.createCategory, name='create_category'),
    path('update_category/<uuid:id>', views.updateCategory, name='update_category'),
    path('delete_category/<uuid:id>', views.deleteCategory, name='delete_category'),
    path('view_products/', views.viewProducts, name='view_products'),
    path('create_product/', views.createProduct, name='create_product'),
    path('each_product/<uuid:id>', views.viewAndUpdateEachProduct, name='each_product'),
    path('delete_product/<uuid:id>', views.deleteProduct, name='delete_product'),
    path('view_category_products/<uuid:id>', views.viewCategoryProducts, name='view_category_products'),
    
    # Service
    path('view_services/', views.viewAndCreateServices, name='view_services'),
    path('update_service/<uuid:id>', views.updateService, name='update_service'),
    path('delete_service/<uuid:id>', views.deleteService, name='delete_service'),
    
    # Servicer
    path('view_servicers/', views.viewServicers, name='view_servicers'),
    path('create_servicer/', views.createServicer, name='create_servicer'),
    path('fetch_employee_filtered/', views.fetchEmployeeFiltered, name='fetch_employee_filtered'),
    path('fetch_servicer/<uuid:selected_employee>', views.fetchServicer, name='fetch_servicer'),
    path('delete_servicer/<uuid:id>', views.deleteServicer, name='delete_servicer'),
    
    # Service Work
    path('view_serviceworks/', views.viewServiceWorks, name='view_serviceworks'),
    path('create_servicework/', views.createServiceWork, name='create_servicework'),
    path('each_service_work/<uuid:id>', views.eachServiceWork, name='each_service_work'),
    path('servicework_change_status/<uuid:id>', views.serviceWorkChangeStatus, name='servicework_change_status'),
    path('delete_service_work/<uuid:id>', views.deleteServiceWork, name='delete_service_work'),
    
    # Test
    path('view_tests/', views.viewTests, name='view_tests'),
    path('create_test/', views.createTest, name='create_test'),
    path('delete_test/<uuid:id>', views.deleteTest, name='delete_test'),
    
    # ServiceWork Assign
    path('view_assigns/', views.viewAssigning, name='view_assigns'),
    path('assign_servicer/<uuid:id>', views.assignServicer, name='assign_servicer'),
    path('unassign_servicer/<uuid:id>', views.unAssignServicer, name='unassign_servicer'),
    
    # Dashboard
    path('', views.viewDashboard, name='view_dashboard'),
    
    # Notification
    # path('notifications/', views.getNotifications, name='notifications'),
    # path('update_notification_status/<uuid:id>', views.updateNotificationStatus, name='update_notification_status'),
    # path('each_notification_read/<uuid:id>', views.markEachNotificationRead, name='each_notification_read'),
    # path('all_notification_read/', views.markAllNotificationsRead, name='all_notification_read'),

]
