from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Employee Functions --------------------------------------------------------------------------------------------------------------------------------
@login_required
def createEmployee(request):
    
    employee_form = EmployeeForm()
    
    if request.method == 'POST':

        employee_form = EmployeeForm(request.POST, request.FILES)
        
        # Generating Employee Code
        employee_codes_only = Employee.objects.values_list('employee_code', flat=True)
        
        max_employee_code = ''
        
        if employee_codes_only.exists():
            max_employee_code = max(employee_codes_only)
        
        employee_code_loop = True
        employee_code_number = 9001
        
        while employee_code_loop:
            
            generated_employee_code = "EMP_" + str(employee_code_number)
        
            if max_employee_code:
                if generated_employee_code in employee_codes_only or int(generated_employee_code[4:]) <= int(max_employee_code[4:]):
                    employee_code_number += 1
                else:
                    break
            else:
                if generated_employee_code in employee_codes_only:
                    employee_code_number += 1
                else:
                    break
        
        if employee_form.is_valid():
            
            employee = employee_form.save(commit=False)
            employee.employee_code = generated_employee_code
            employee.save()
            return redirect('purifier:view_employees')
        
        else:
            print(employee_form.errors)
    
    context = {'employee_form': employee_form}
            
    return render(request, 'employee/employee.html', context)

@login_required
def viewEmployees(request):
    
    employees = Employee.objects.all().order_by('-employee_code')
    employees_exists = employees.exists()
    
    context = {'employees': employees, 'employees_exists': employees_exists}
    
    return render(request, 'employee/view_employees.html', context)

@login_required
def eachEmployee(request, id):
    
    employee = get_object_or_404(Employee, pk=id)
    
    context = {'employee': employee}
    
    return render(request, 'employee/each_employee.html', context)

@login_required
def updateEmployee(request, id):
    
    employee = get_object_or_404(Employee, pk=id)
    
    employee_form = EmployeeForm(instance=employee)
    
    employee_code_stored = employee.employee_code
    employee_pass_stored = employee.initial_password

    if request.method == 'POST':
        
        employee_form = EmployeeForm(request.POST, request.FILES, instance=employee)
        
        if employee_form.is_valid():
            
            employee_save = employee_form.save(commit=False)
            
            employee_save.employee_code = employee_code_stored
            employee_save.initial_password = employee_pass_stored
            
            employee_save.save()
            
            return redirect(reverse('purifier:each_employee', kwargs={'id': employee.id}))
        
    context = {'employee_form': employee_form, 'employee': employee}
        
    return render(request, 'employee/employee.html', context)

@login_required
def deleteEmployee(request, id):
    
    employee = get_object_or_404(Employee, pk=id)
    employee.delete()

    return redirect('purifier:view_employees')


# Customer Functions --------------------------------------------------------------------------------------------------------------------------------
@login_required
def createCustomer(request):
    
    customer_form = CustomerForm()
    
    if request.method == 'POST':
        
        customer_form = CustomerForm(request.POST, request.FILES)
        
        # Generating Customer Code
        customer_codes_only = Customer.objects.values_list('customer_code', flat=True)
        
        max_customer_code = ""
        
        if customer_codes_only.exists():
            max_customer_code = max(customer_codes_only)
        
        customer_code_loop = True
        customer_code_number = 1001
        
        while customer_code_loop:
            
            generated_customer_code = "CUS_" + str(customer_code_number)
        
            if max_customer_code:
                if generated_customer_code in customer_codes_only or int(generated_customer_code[4:]) <= int(max_customer_code[4:]):
                    customer_code_number += 1
                else:
                    break
            else:
                if generated_customer_code in customer_codes_only:
                    customer_code_number += 1
                else:
                    break
            
        if customer_form.is_valid():
            
            customer = customer_form.save(commit=False)
            customer.customer_code = generated_customer_code
 
            customer.save()
            
            installed_products = request.POST.getlist('installed_product')
            customer.installed_product.set(installed_products)
            
            return redirect('purifier:view_customers')
        
    context = {'customer_form': customer_form}
            
    return render(request, 'customer/customer.html', context)

@login_required
def viewCustomers(request):
    
    customers = Customer.objects.all().order_by('-customer_code')
    customers_exists = customers.exists()
    
    context = {'customers': customers, 'customers_exists': customers_exists}
    
    return render(request, 'customer/view_customers.html', context)

@login_required
def eachCustomer(request , id):
    
    customer = get_object_or_404(Customer, pk=id)
    
    customer_products = CustomerProduct.objects.filter(customer_code=customer).order_by('-created_on')
    
    context = {'customer': customer, 'customer_products': customer_products}
    
    return render(request, 'customer/each_customer.html', context)

@login_required
def updateCustomer(request , id):
    
    customer = get_object_or_404(Customer, pk=id)
    
    customer_form = CustomerForm(instance=customer)
    
    customer_code_stored = customer.customer_code
    customer_pass_stored = customer.initial_password
    
    if request.method == 'POST':
        
        customer_form = CustomerForm(request.POST, request.FILES, instance=customer)
        
        if customer_form.is_valid():
            
            customer_save = customer_form.save(commit=False)
            customer_save.customer_code = customer_code_stored
            customer_save.initial_password = customer_pass_stored
            customer_save.save() 
            
            installed_products = request.POST.getlist('installed_product')
            customer.installed_product.set(installed_products)
            
            return redirect(reverse('purifier:each_customer', kwargs={'id': customer.id}))
        
    context = {'customer_form': customer_form, 'customer': customer}
    
    return render(request, 'customer/customer.html', context)

@login_required
def deleteCustomer(request, id):
    
    customer = get_object_or_404(Customer, pk=id)
    customer.delete()
    return redirect('purifier:view_customers')


# Product Functions ---------------------------------------------------------------------------------------------------------------------------------
@login_required
def viewCategories(request):
    
    categories = Category.objects.all()
    
    categories_exists = categories.exists()
    
    category_form = CategoryForm()
    
    context = {'categories': categories, 'categories_exists': categories_exists, 'category_form': category_form}
    
    return render(request, 'product/category.html', context)

@login_required
def createCategory(request):
    
    if request.method == 'POST':
        
        category_form = CategoryForm(request.POST, request.FILES)
        
        if category_form.is_valid():
            
            category_form.save()
            
        return redirect('purifier:view_products')

@login_required
def updateCategory(request, id):
    
    category = get_object_or_404(Category, pk=id)
    
    category_form = CategoryForm(instance=category)
    
    if request.method == 'POST':
        
        category_form = CategoryForm(request.POST, request.FILES, instance=category)
        
        if category_form.is_valid():
            
            category_form.save()
            
            return redirect('purifier:view_categories')
        
    context = {'category': category, 'category_form': category_form}
        
    return render(request, 'product/category.html',context)

@login_required
def deleteCategory(request, id):
    
    category = get_object_or_404(Category, pk=id)
    category.delete()
    return redirect('purifier:view_categories')

@login_required
def createProduct(request):
    
    if request.method == 'POST':
        
        product_form = ProductForm(request.POST, request.FILES)
        
        if product_form.is_valid():
            
            product_form.save()
            
            return redirect('purifier:view_products')   
    
    return render(request, 'product/product.html')

@login_required
def viewProducts(request):
    
    category_form = CategoryForm()
    
    product_form = ProductForm()
    
    products = Product.objects.all()
    
    products_exists = products.exists()
    
    context = {'category_form': category_form, 'product_form': product_form, 'products': products, 'products_exists': products_exists}
    
    return render(request, 'product/product.html', context)

@login_required
def viewAndUpdateEachProduct(request, id):
    
    product = get_object_or_404(Product, pk=id)
    
    product_form = ProductForm(instance=product)
    
    if request.method == 'POST':
    
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        
        if product_form.is_valid():
            
            product_form.save()
            
            return redirect(reverse('purifier:each_product', kwargs={'id': product.id}))
    
    context = {'product_form': product_form, 'product': product}
    
    return render(request, 'product/each_product.html', context)

@login_required
def deleteProduct(request, id):
    
    product = get_object_or_404(Product, pk=id)
    
    product.delete()
    
    return redirect('purifier:view_products')

@login_required
def viewCategoryProducts(request, id):
    
    print("getting in")
 
    if request.method == 'GET':
        
        try:
            products = Product.objects.filter(category=id)
            
            category = get_object_or_404(Category, pk=id)
            
            category_data = {'name': category.name}
            
            products_exists = products.exists()
            
            products_data = [{'id': product.id, 'product_serial': product.product_serial, 'name': product.name} for product in products]
            
            data = {
                'category_products': products_data,
                'category_products_exists': products_exists,
                'category': category_data,
            }
            return JsonResponse(data)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Products not found'}, status=404)
            

# Service Functions --------------------------------------------------------------------------------------------------------------------------------
@login_required
def viewAndCreateServices(request):
    
    services = Service.objects.all()
    services_exists = services.exists()
    
    service_form = ServiceForm()
    
    if request.method == 'POST':
        
        service_form = ServiceForm(request.POST)
        
        if service_form.is_valid():
            
            service_form.save()
            
            return redirect('purifier:view_services')
    
    context = {'services': services, 'services_exists': services_exists, 'service_form': service_form}
    return render(request, 'service/view_services.html', context)

@login_required
def updateService(request, id):
    
    service = get_object_or_404(Service, pk=id)
    
    service_form = ServiceForm(instance=service)
    
    if request.method == 'POST':
        
        service_form = ServiceForm(request.POST, instance=service)
        
        if service_form.is_valid():
            
            service_form.save()
            
            return redirect('purifier:view_services')

@login_required
def deleteService(request, id):
    
    service = get_object_or_404(Service, pk=id)
    service.delete()
    return redirect('purifier:view_services')


# Servicer Functions --------------------------------------------------------------------------------------------------------------------------------
@login_required
def viewServicers(request):
    
    servicers = Servicer.objects.all().order_by('-name__employee_code')
    
    servicers_exists = servicers.exists()
    
    servicer_form = ServicerForm()
    
    context = {'servicers': servicers, 'servicers_exists': servicers_exists, 'servicer_form': servicer_form}
    
    return render(request, 'servicer/view_servicers.html', context)

@login_required
def createServicer(request):
    
    if request.method == 'POST':
        
        servicer_form = ServicerForm(request.POST)
        
        if servicer_form.is_valid():
            
            servicer_form.save()
            
            return redirect('purifier:view_servicers')
        
    return render(request, 'servicer/view_servicers.html')

@login_required
def fetchEmployeeFiltered(request):
    
    if request.method == 'GET':
        
        try:
            servicers = Servicer.objects.all()
            
            employees = Employee.objects.exclude(id__in=servicers.values('name_id'))
            
            employees_exists = employees.exists()
            
            employees_data = [{'id': employee.id, 'name': employee.name} for employee in employees]
            
            data = {
                'employees': employees_data,
                'employees_exists': employees_exists,
            }
            return JsonResponse(data)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)

@login_required
def fetchServicer(request, selected_employee):
    
    if request.method == 'GET':
    
        try:
            employee = Employee.objects.get(pk=selected_employee)
            data = {'employee': {
                'employee_code': employee.employee_code,
                'mobile': employee.mobile,
                # Add other fields as needed
            }}
            return JsonResponse(data)
        except Employee.DoesNotExist:
            return JsonResponse({'error': 'Employee not found'}, status=404)
        
@login_required
def deleteServicer(request, id):
    
    servicer = get_object_or_404(Servicer, pk=id)
    servicer.delete()
    return redirect('purifier:view_servicers')
        

# Service Work Functions ----------------------------------------------------------------------------------------------------------------------------
@login_required
def viewServiceWorks(request):
    
    service_works = ServiceWork.objects.all().order_by('-service_work_code')
    
    service_works_exists = service_works.exists()
    
    service_work_form = ServiceWorkForm()
    
    
    if request.method == 'GET':
            
        filter_customer = request.GET.get('customerSelect')
        
        selected_customer = request.GET.get('selectedCustomer')
        
        selected_product = request.GET.get('selectedProduct')
        
        try:
            # filter products
            if selected_customer:

                customer = get_object_or_404(Customer, pk=selected_customer)
                installed_products = customer.installed_product.all()

                products = Product.objects.filter(id__in=installed_products)
                
                products_data = [{'id': product.id, 'name': product.name, 'product_serial': product.product_serial} for product in products]
                
                data = {
                    'products': products_data,
                }
                return JsonResponse(data)
            
            # filter services
            if selected_product:
                
                product = get_object_or_404(Product, pk=selected_product)
                product_services = product.services.all()
                
                services = Service.objects.filter(id__in=product_services)
                
                services_data = [{'id': service.id, 'name': service.name} for service in services]
                
                data = {
                    'services': services_data,
                }
                
                return JsonResponse(data)
            
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Customer.DoesNotExist:
                return JsonResponse({'error': 'Customer not found'}, status=404)
    
    context = {'service_works': service_works, 'service_works_exists': service_works_exists, 'service_work_form': service_work_form}
    
    return render(request, 'servicework/view_serviceworks.html', context)

@login_required
def createServiceWork(request):
    
    service_work_form = ServiceWorkForm()
    
    if request.method == 'POST':
        
        service_work_form = ServiceWorkForm(request.POST)
    
        # Generating Service Work Code
        servicework_codes_only = ServiceWork.objects.values_list('service_work_code', flat=True)
        
        max_servicework_code = ''
        
        if servicework_codes_only.exists():
            max_servicework_code = max(servicework_codes_only)
        
        servicework_code_loop = True
        servicework_code_number = 1
        
        while servicework_code_loop:
            
            if servicework_code_number < 1000:
                servicework_code_leading_zeros = 4 - len(str(servicework_code_number))
                servicework_code = "0" * servicework_code_leading_zeros + str(servicework_code_number)
            else:
                servicework_code = str(servicework_code_number)
            
            generated_servicework_code = "SC_" + servicework_code
        
            if max_servicework_code:
                if generated_servicework_code in servicework_codes_only or int(generated_servicework_code[3:]) <= int(max_servicework_code[3:]):
                    servicework_code_number += 1
                else:
                    break
            else:
                if generated_servicework_code in servicework_codes_only:
                    servicework_code_number += 1
                else:
                    break
        
        if service_work_form.is_valid():
            
            servicework = service_work_form.save(commit=False)
            
            servicework.service_work_code = generated_servicework_code

            servicework.save()
            
            servicework.service_name.clear()
            selected_service_names = request.POST.getlist('service_name')
            for service_name_id in selected_service_names:
                servicework.service_name.add(service_name_id)
            
            servicework_toassign = ServiceAssign(service=servicework)
            
            servicework_toassign.save()
            
            return redirect('purifier:view_serviceworks')
        
        else:
            print(service_work_form.errors)
            
    context = {'service_work_form': service_work_form}
    
    return render(request, 'servicework/servicework.html', context)
        
@login_required
def eachServiceWork(request, id):
    
    service_work = get_object_or_404(ServiceWork, pk=id)
    
    service_work_form = ServiceWorkForm(instance=service_work)
    
    service_work_code_stored = service_work.service_work_code
    
    
    # fetching and passing using ajax
    if request.method == 'GET':
        
        selected_customer = request.GET.get('selectedCustomer')
        
        selected_product = request.GET.get('selectedProduct')
        
    
        try:
            if selected_customer:
                    
                customer = get_object_or_404(Customer, pk=selected_customer)
                installed_products = customer.installed_product.all()

                products = Product.objects.filter(id__in=installed_products)
                
                products_data = [{'id': product.id, 'name': product.name} for product in products]
                
                data = {
                    'products': products_data,
                }
                return JsonResponse(data)
            
            if selected_product:

                product = get_object_or_404(Product, pk=selected_product)
                product_services = product.services.all()
                
                services = Service.objects.filter(id__in=product_services)
                
                default_services = service_work.service_name.all()
                
                default_services_data = [{'id': default_service.id, 'name': default_service.name} for default_service in default_services]
                
                services_data = [{'id': service.id, 'name': service.name} for service in services]
                
                data = {
                    'services': services_data,
                    'default_services': default_services_data,
                }
                
                return JsonResponse(data)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=404)
            
    
    if request.method == 'POST':
        
        service_work_form = ServiceWorkForm(request.POST, instance=service_work)
        
        if service_work_form.is_valid():
            
            service_work_save = service_work_form.save(commit=False)
            service_work_save.service_work_code = service_work_code_stored
            service_work_save.save()
            
            service_work.service_name.clear()
            selected_service_names = request.POST.getlist('service_name')
            
            for service_name_id in selected_service_names:
                service_work.service_name.add(service_name_id)
            
            return redirect(reverse('purifier:each_service_work', kwargs={'id': service_work.id}))
    
    context = {'service_work': service_work, 'service_work_form': service_work_form}
    
    return render(request, 'servicework/each_servicework.html', context)

@login_required
def serviceWorkChangeStatus(request, id):
    
    servicework = get_object_or_404(ServiceWork, pk=id)
    
    print(servicework)
    
    current_work_status = servicework.status
    
    print(current_work_status)
    
    if current_work_status == 'pending':
        
        servicework.status = 'working'
            
    elif current_work_status == 'working':
        
        servicework.status = 'completed'
    
    elif current_work_status == 'completed':
        
        servicework.status = 'pending'
        
    else:
        
        print(f"Unknown status: {current_work_status}")
        
    servicework.save()
    
    # html_content = render(request, 'servicework/each_servicework.html', {'servicework': servicework}).content
    
    return JsonResponse({'servicework': servicework})
        
    # return redirect(reverse('purifier:each_service_work', kwargs={'id': servicework.id}))

@login_required
def deleteServiceWork(request, id):
    
    servicework = get_object_or_404(ServiceWork, pk=id)
    servicework.delete()
    return redirect('purifier:view_serviceworks')


# Service Assign Functions --------------------------------------------------------------------------------------------------------------------------
@login_required
def viewAssigning(request):
    
    servicework_assign_form = ServiceWorkAssignForm()
    
    serviceworks_toassign = ServiceAssign.objects.all().order_by('-service__service_work_code')
    
    serviceworks_toassign_exists = serviceworks_toassign.exists()
    
    servicers = Servicer.objects.all() 
    
    servicers_exists = servicers.exists()
    
    context = {'servicework_assign_form': servicework_assign_form, 'serviceworks_toassign': serviceworks_toassign, 'serviceworks_toassign_exists':serviceworks_toassign_exists, 'servicers_exists': servicers_exists}
    
    return render(request, 'service_assigning/view_assigning.html', context) 

@login_required
def assignServicer(request, id):
    
    servicework = get_object_or_404(ServiceAssign, pk=id)
    
    assigned_servicework = servicework.service
    
    if request.method == 'POST':
        
        servicework_assign_form = ServiceWorkAssignForm(request.POST, instance=servicework)
        
        if servicework_assign_form.is_valid():
            
            save_form = servicework_assign_form.save(commit=False)
            
            save_form.service = assigned_servicework
            
            save_form.save()
            
            return redirect('purifier:view_assigns')
        
    return redirect('purifier:view_assigns')

@login_required
def unAssignServicer(request, id):
    
    service_assigned = get_object_or_404(ServiceAssign, pk=id)
    
    service_assigned.servicer = None
    
    service_assigned.save()
    
    return redirect('purifier:view_assigns')


# Test or Quality check Functions -------------------------------------------------------------------------------------------------------------------
@login_required
def viewTests(request):
    
    tests = Test.objects.all().order_by('-created_on')
    
    tests_exists = tests.exists()
    
    context = {'tests': tests, 'tests_exists': tests_exists}
    
    return render(request, 'test/view_tests.html', context)

@login_required
def createTest(request):
    
    test_form = TestForm()
    
    if request.method == 'POST':
        
        test_form = TestForm(request.POST)
        
        if test_form.is_valid():
            
            test_form.save()
            
            return redirect('purifier:view_tests')
        
    context = {'test_form': test_form}
        
    return render(request, 'test/test.html', context)

@login_required
def deleteTest(request, id):
    
    test = get_object_or_404(Test, pk=id)
    test.delete()
    return redirect('purifier:view_tests')


# Dashboard Functions -------------------------------------------------------------------------------------------------------------------------------
@login_required
def viewDashboard(request):
    
    today_date = timezone.now().date()

    servicework_today = ServiceWork.objects \
    .exclude(status='completed') \
    .filter(service_date=today_date) \
    .order_by('-service_work_code')
    
    servicework_today_exists = servicework_today.exists()
    servicework_today_count = servicework_today.count()
    
    servicework_pending = ServiceWork.objects.exclude(status='completed')
    servicework_pending_exists = servicework_pending.exists()
    pending_count = servicework_pending.count()
    
    servicework_upcoming = ServiceWork.objects \
    .exclude(service_date=today_date) \
    .filter(status='pending') \
    .order_by('-service_work_code')
    servicework_upcoming_exists = servicework_upcoming.exists()
    upcoming_count = servicework_upcoming.count()
    
    servicework_completed = ServiceWork.objects.filter(status='completed').order_by('-service_work_code')
    completed_count = servicework_completed.count()
    
    customers_count =Customer.objects.all().count()
    employees_count = Employee.objects.all().count()
    products_count = Product.objects.all().count()

    
    context = {'servicework_today': servicework_today, 'servicework_completed': servicework_completed, 'servicework_pending': servicework_pending, 'servicework_pending_exists': servicework_pending_exists, 'servicework_today_exists': servicework_today_exists, 'servicework_upcoming': servicework_upcoming, 'servicework_upcoming_exists': servicework_upcoming_exists, 'completed_count': completed_count, 'upcoming_count': upcoming_count, 'pending_count': pending_count,'customers_count': customers_count, 'employees_count': employees_count, 'products_count': products_count, 'servicework_today_count': servicework_today_count}
    
    return render(request, 'dashboard/dashboard.html', context)


# Notification Functions ----------------------------------------------------------------------------------------------------------------------------
# def getNotifications(request):

#     if request.method == 'GET':
            
#         try:
#             notifications = Notification.objects.filter(is_read=False).order_by('-timestamp')
            
#             notification_data = [{'id': notification.id, 'message': notification.message, 'message_of': notification.message_of, 'once_passed':notification.once_passed, 'timestamp': notification.timestamp} for notification in notifications]
            
#             data = {
#                 'notification_data': notification_data,
#             }
#             return JsonResponse(data)
#         except Notification.DoesNotExist:
#             return JsonResponse({'error': 'Notification not found'}, status=404)
        
# def updateNotificationStatus(request, id):

#     if request.method == 'POST':
#         try:
#             notification = get_object_or_404(Notification, pk=id)
#             notification.once_passed = True
#             notification.save()
#             return JsonResponse({'success': True})
#         except Notification.DoesNotExist:
#             return JsonResponse({'error': 'Notification not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)
    
# def markEachNotificationRead(request, id):
    
#     notification = get_object_or_404(Notification, pk=id)
#     notification.delete()
#     return f"Notification read."
    
# def markAllNotificationsRead(request):
    
    notifications = Notification.objects.filter(is_read=False, once_passed=True)
    notifications.delete()
    return HttpResponse(status=204)