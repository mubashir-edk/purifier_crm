from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        
        widgets = {
            'profile': forms.FileInput(attrs={
                'id': 'formEmployeeProfile',
                'class': '',
            }),
            'name': forms.TextInput(attrs={
                'id': 'formEmployeeName', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Employee Name',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'formEmployeeEmail', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Email Address',
            }),
            'mobile': forms.TextInput(attrs={
                'id': 'formEmployeeMobile',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Mobile Number',
            }),
            'address': forms.Textarea(attrs={
                'id': 'formEmployeeAddress',
                'class': 'block bg-white p-2.5 w-full text-sm rounded-lg border-none focus:ring-blue-500',
                'rows': '4',
                'placeholder': 'Address...',
            }),
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        
        widgets = {
            'profile': forms.FileInput(attrs={
                'id': 'formCustomerProfile',
                'class': '',
            }),
            'name': forms.TextInput(attrs={
                'id': 'formCustomerName', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Customer Name',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'formCustomerEmail', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Email Address',
            }),
            'mobile': forms.TextInput(attrs={
                'id': 'formCustomerMobile',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Mobile Number',
            }),
            'address': forms.Textarea(attrs={
                'id': 'formCustomerAddress', 
                'class': 'block bg-white p-2.5 w-full text-sm rounded-lg border-none focus:ring-blue-500',
                'rows': '4',
                'placeholder': 'Address...',
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'id': 'formCustomerWhatsappNumber', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Whatsapp Number',
            }),
            'installed_product': forms.CheckboxSelectMultiple(attrs={
                'id': 'formCustomerInstalledProduct', 
                'class': 'w-4 h-4 text-black border-gray-300 rounded',
            }),
            'location': forms.TextInput(attrs={
                'id': 'formCustomerLocation', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
            }),
        }
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
        widgets = {
            'image': forms.FileInput(attrs={
                'id': 'formCategoryImage',
                'class': '',
            }),
            'name': forms.TextInput(attrs={
                'id': 'formCategoryName',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Category Name',
            }),
        }
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        widgets = {
            'product_serial': forms.TextInput(attrs={
                'id': 'formProductSerial',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Product Serial',
            }),
            'category': forms.Select(attrs={
                'id': 'formProductCategory',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
            }),
            'name': forms.TextInput(attrs={
                'id': 'formProductName',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Product Name',
            }),
            'image': forms.FileInput(attrs={
                'id': 'formProductImage',
                'class': '',
            }),
            'services': forms.CheckboxSelectMultiple(attrs={
                'id': 'formProductServices',
                'class': 'w-4 h-4 text-black border-gray-300 rounded',
            }),
        }
        
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
        
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'formServiceName',
                'class': 'block bg-white p-2.5 w-full text-sm rounded-lg border-none focus:ring-blue-500',
                'placeholder': 'Service Name',
            }),
        }
        
class ServicerForm(forms.ModelForm):
    class Meta:
        model = Servicer
        fields = '__all__'
        
        widgets = {
            'name': forms.Select(attrs={
                'id': 'formServicerName',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].queryset = Employee.objects.all()
        self.fields['name'].label_from_instance = lambda obj: f"{obj.name}"
        
class ServiceWorkForm(forms.ModelForm):
    class Meta:
        model = ServiceWork
        exclude = ('status',)
        
        
        widgets = {
            'customer_code': forms.Select(attrs={
                'id': 'formServiceWorkCustomer',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',    
            }),
            'product': forms.Select(attrs={
                'id': 'formServiceWorkProduct',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',    
            }),
            'service_name': forms.CheckboxSelectMultiple(attrs={
                'id': 'formServiceWorkService',   
                'class': 'w-4 h-4 text-black border-gray-300 rounded',    
            }),
            'comment_section': forms.Textarea(attrs={
                'id': 'formServiceWorkComment',
                'class': 'block bg-white p-2.5 w-full text-sm rounded-lg border-none focus:ring-blue-500',
                'rows': '4',
                'placeholder': 'Comments...',
            }),
            'service_date': forms.DateInput(attrs={
                'id': 'formServiceWorkDate',    
                'class': 'block bg-white ps-10 p-2.5 w-full text-sm rounded-lg border-none focus:ring-blue-500',   
                'placeholder': 'Select Date',  
                'autocomplete': 'off',     
                'datepicker': True,     
            }),
            'remark_section': forms.Textarea(attrs={
                'id': 'formServiceWorkRemark',
                'class': 'block bg-white p-2.5 w-full text-sm rounded-lg border-none focus:ring-blue-500',
                'rows': '4',
                'placeholder': 'Remark...',
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter customer_code queryset to exclude customers with empty products
        self.fields['customer_code'].queryset = self.fields['customer_code'].queryset.exclude(installed_product=None)
        
class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = '__all__'
        
        
        widgets = {
            'test_name': forms.TextInput(attrs={
                'id': 'formTestName',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',   
                'placeholder': 'Test Name', 
            }),
            'customer_code': forms.Select(attrs={
                'id': 'formTestCustomerCode',     
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',   
            }),
            'ph_value': forms.TextInput(attrs={
                'id': 'formPhValue',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5', 
                'placeholder': 'PH Value',   
            }),
            'tds_value': forms.TextInput(attrs={
                'id': 'formTdsValue',
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'TDS Value',    
            }),
            'iron_value': forms.TextInput(attrs={
                'id': 'formIronValue',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',
                'placeholder': 'Iron Value',     
            }),
            'hardness_value': forms.TextInput(attrs={
                'id': 'formHardnessValue',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5', 
                'placeholder': 'Hardness Value',   
            }),
            'turbuet_value': forms.TextInput(attrs={
                'id': 'formTurbuetValue', 
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5', 
                'placeholder': 'Turbuet Value',   
            }),
        }
        
class ServiceWorkAssignForm(forms.ModelForm):
    class Meta:
        model = ServiceAssign
        fields = '__all__'
        
        widgets = {
            'service': forms.Select(attrs={
                'id': 'formAssignService',    
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',     
            }),
            'servicer': forms.Select(attrs={
                'id': 'formAssignServicer',     
                'class': 'bg-white text-gray-900 text-sm rounded-lg border-none focus:ring-blue-500 block w-full p-2.5',     
            }),
        }