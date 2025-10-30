"""
Utility functions for user activity tracking
"""

from .models import UserActivity


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_user_agent(request):
    """Get user agent from request"""
    return request.META.get('HTTP_USER_AGENT', '')


def log_user_activity(user, action, request=None, details=None):
    """
    Log user activity for admin monitoring
    
    Args:
        user: User instance
        action: Action type (from UserActivity.ACTION_CHOICES)
        request: HttpRequest instance (optional)
        details: Additional details dictionary (optional)
    """
    if user and user.is_authenticated:
        activity_data = {
            'user': user,
            'action': action,
            'details': details or {}
        }
        
        if request:
            activity_data['ip_address'] = get_client_ip(request)
            activity_data['user_agent'] = get_user_agent(request)
        
        UserActivity.objects.create(**activity_data)
