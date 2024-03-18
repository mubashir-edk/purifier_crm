from rest_framework.permissions import BasePermission

class CustomIsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users of a specific type (e.g., employee or customer).
    """
    def has_permission(self, request, view):
        print(request.user)
        return (
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_employee or request.user.is_customer)
        )
        
class EmployeeIsAuthenticated(BasePermission):
    """
    Allows access only to authenticated user type employee
    """
    def has_permission(self, request, view):
        print(request.user)
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_employee
        )
        
class CustomerIsAuthenticated(BasePermission):
    """
    Allows access only to authenticated user type customer
    """
    def has_permission(self, request, view):
        print(request.user)
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.is_customer
        )
        
        