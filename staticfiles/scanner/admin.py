from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from django import forms
from .models import ScanReport, UserActivity


# Unregister the default User admin
admin.site.unregister(User)


class CustomUserForm(forms.ModelForm):
    """Custom form to make password field user-friendly"""
    password = forms.CharField(
        label='Password',
        help_text='Enter new password (will be automatically hashed)',
        widget=forms.TextInput(attrs={'placeholder': 'Enter new password or leave unchanged'}),
        required=False
    )
    
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Enhanced User admin with activity tracking and security features"""
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 
                   'last_login', 'date_joined', 'scan_count', 'recent_activity', 'password_display', 'user_actions')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    readonly_fields = ('last_login', 'date_joined', 'scan_count_display', 'recent_activity_display')
    
    # Use custom form for password editing
    form = CustomUserForm
    
    # Add actions for promoting/demoting users
    actions = ['make_admin', 'remove_admin']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Activity Summary', {
            'fields': ('scan_count_display', 'recent_activity_display'),
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make password readonly but allow editing other fields"""
        readonly = list(self.readonly_fields)
        if obj:  # editing an existing object
            readonly.extend(['user_actions'])
        return readonly
    
    def user_actions(self, obj):
        """Individual action buttons for each user"""
        if obj.pk:  # Only show for existing users
            buttons = []
            
            # Make/Remove Admin button
            if obj.is_superuser:
                buttons.append(
                    f'<a href="?action=remove_admin_single&user_id={obj.pk}" '
                    f'style="background: #dc3545; color: white; padding: 3px 6px; border-radius: 3px; text-decoration: none; font-size: 10px; margin-right: 4px; display: inline-block; white-space: nowrap;" '
                    f'onclick="return confirm(\'Remove admin status from {obj.username}?\')">Remove Admin</a>'
                )
            else:
                buttons.append(
                    f'<a href="?action=make_admin_single&user_id={obj.pk}" '
                    f'style="background: #28a745; color: white; padding: 3px 6px; border-radius: 3px; text-decoration: none; font-size: 10px; margin-right: 4px; display: inline-block; white-space: nowrap;" '
                    f'onclick="return confirm(\'Make {obj.username} an admin?\')">Make Admin</a>'
                )
            
            # Change Password button
            buttons.append(
                f'<a href="#" '
                f'style="background: #17a2b8; color: white; padding: 3px 6px; border-radius: 3px; text-decoration: none; font-size: 10px; margin-right: 4px; display: inline-block; white-space: nowrap;" '
                f'onclick="var newPass = prompt(\'Enter new password for {obj.username}:\'); if(newPass) {{{{ window.location.href = \'?action=change_password_single&user_id={obj.pk}&new_password=\' + encodeURIComponent(newPass); }}}} return false;">Change Password</a>'
            )
            
            # Delete User button (only if not current user)
            buttons.append(
                f'<a href="?action=delete_user_single&user_id={obj.pk}" '
                f'style="background: #6c757d; color: white; padding: 3px 6px; border-radius: 3px; text-decoration: none; font-size: 10px; margin-right: 4px; display: inline-block; white-space: nowrap;" '
                f'onclick="return confirm(\'Are you sure you want to DELETE {obj.username}? This action cannot be undone!\')">Delete</a>'
            )
            
            return format_html('<div style="min-width: 200px;">{}</div>'.format(''.join(buttons)))
        return "-"
    user_actions.short_description = 'Actions'
    user_actions.allow_tags = True
    
    def scan_count(self, obj):
        """Get user's total scan count"""
        return obj.scanreport_set.count()
    scan_count.short_description = 'Total Scans'
    
    def scan_count_display(self, obj):
        """Get user's total scan count for detail view"""
        return obj.scanreport_set.count()
    scan_count_display.short_description = 'Total Scans'
    
    def recent_activity(self, obj):
        """Show recent activity status"""
        recent_cutoff = timezone.now() - timedelta(days=7)
        recent_activities = obj.activities.filter(timestamp__gte=recent_cutoff).count()
        if recent_activities > 0:
            return format_html('<span style="color: green;">Active ({})</span>', recent_activities)
        return format_html('<span style="color: orange;">Inactive</span>')
    recent_activity.short_description = 'Recent Activity'
    
    def recent_activity_display(self, obj):
        """Display recent activities for detail view"""
        activities = obj.activities.all()[:5]
        if activities:
            activity_list = []
            for activity in activities:
                activity_list.append(f"{activity.get_action_display()} - {activity.timestamp.strftime('%Y-%m-%d %H:%M')}")
            return format_html('<br>'.join(activity_list))
        return "No recent activity"
    recent_activity_display.short_description = 'Recent Activities'
    
    def password_display(self, obj):
        """Display actual password for admin viewing in list"""
        # Check if user has a stored plain password in UserActivity or create a method to track it
        from .models import UserActivity
        
        # Try to get the last password change activity
        password_activity = UserActivity.objects.filter(
            user=obj, 
            action='password_changed'
        ).order_by('-timestamp').first()
        
        if password_activity and password_activity.details and 'password' in password_activity.details:
            actual_password = password_activity.details['password']
            return format_html(
                '<div style="font-family: monospace; font-size: 0.8em; max-width: 150px;">'
                '<div style="font-weight: bold; color: #d63384; background: #f8f9fa; padding: 2px 4px; border-radius: 2px;">{}</div>'
                '<button onclick="navigator.clipboard.writeText(\'{}\'); alert(\'Password copied!\');" '
                'style="margin-top: 2px; padding: 1px 4px; background: #198754; color: white; border: none; border-radius: 2px; cursor: pointer; font-size: 10px;">'
                'Copy</button>'
                '</div>',
                actual_password,
                actual_password
            )
        else:
            # For existing users without tracked passwords, show username as default
            return format_html(
                '<div style="font-family: monospace; font-size: 0.8em; max-width: 150px;">'
                '<div style="font-weight: bold; color: #6c757d; background: #f8f9fa; padding: 2px 4px; border-radius: 2px;">{}</div>'
                '<small style="color: #6c757d;">Default</small>'
                '</div>',
                obj.username
            )
    password_display.short_description = 'Password'
    
    def make_admin(self, request, queryset):
        """Make selected users admin"""
        updated = 0
        for user in queryset:
            if not user.is_staff or not user.is_superuser:
                user.is_staff = True
                user.is_superuser = True
                user.save()
                updated += 1
        self.message_user(request, f'{updated} users promoted to admin status.')
    make_admin.short_description = "Promote selected users to admin"
    
    def remove_admin(self, request, queryset):
        """Remove admin status from selected users"""
        updated = 0
        for user in queryset:
            if user.is_staff or user.is_superuser:
                user.is_staff = False
                user.is_superuser = False
                user.save()
                updated += 1
        self.message_user(request, f'{updated} users demoted from admin status.')
    remove_admin.short_description = "Remove admin status from selected users"
    
    
    def changelist_view(self, request, extra_context=None):
        """Handle individual user actions"""
        # Handle individual actions
        action = request.GET.get('action')
        user_id = request.GET.get('user_id')
        
        if action and user_id:
            try:
                user = User.objects.get(pk=user_id)
                
                if action == 'make_admin_single':
                    user.is_staff = True
                    user.is_superuser = True
                    user.save()
                    self.message_user(request, f'Successfully promoted {user.username} to admin.')
                    
                elif action == 'remove_admin_single':
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    self.message_user(request, f'Successfully removed admin status from {user.username}.')
                    
                elif action == 'change_password_single':
                    new_password = request.GET.get('new_password')
                    if new_password:
                        from django.contrib.auth.hashers import make_password
                        from .models import UserActivity
                        
                        # Store the actual password for admin viewing
                        UserActivity.objects.create(
                            user=user,
                            action='password_changed',
                            ip_address=request.META.get('REMOTE_ADDR', ''),
                            user_agent=request.META.get('HTTP_USER_AGENT', ''),
                            details={'password': new_password, 'changed_by': request.user.username}
                        )
                        
                        user.password = make_password(new_password)
                        user.save()
                        self.message_user(request, f'Successfully changed password for {user.username}.')
                    else:
                        self.message_user(request, 'No password provided.', level='ERROR')
                        
                elif action == 'delete_user_single':
                    # Safety check: prevent deleting current user or last superuser
                    if user == request.user:
                        self.message_user(request, 'You cannot delete yourself.', level='ERROR')
                    elif user.is_superuser and User.objects.filter(is_superuser=True).count() <= 1:
                        self.message_user(request, 'Cannot delete the last superuser.', level='ERROR')
                    else:
                        username = user.username
                        user.delete()
                        self.message_user(request, f'Successfully deleted user {username}.')
                    
            except User.DoesNotExist:
                self.message_user(request, 'User not found.', level='ERROR')
        
        return super().changelist_view(request, extra_context)
    
    def save_model(self, request, obj, form, change):
        """Handle password changes"""
        if 'password' in form.changed_data:
            from django.contrib.auth.hashers import make_password
            from .models import UserActivity
            
            new_password = form.cleaned_data['password']
            
            # Store the actual password for admin viewing
            UserActivity.objects.create(
                user=obj,
                action='password_changed',
                ip_address=request.META.get('REMOTE_ADDR', ''),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                details={'password': new_password, 'changed_by': request.user.username}
            )
            
            # Hash the new password
            obj.password = make_password(new_password)
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.prefetch_related('scanreport_set', 'activities')


@admin.register(ScanReport)
class ScanReportAdmin(admin.ModelAdmin):
    list_display = ('url', 'user', 'result', 'confidence', 'timestamp', 'user_link')
    list_filter = ('result', 'timestamp', 'user__is_staff')
    search_fields = ('url', 'user__username')
    readonly_fields = ('timestamp', 'features_display')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Scan Information', {
            'fields': ('url', 'user', 'result', 'confidence', 'timestamp')
        }),
        ('Technical Details', {
            'fields': ('features_display',),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """Create link to user admin page"""
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.pk])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return "Anonymous"
    user_link.short_description = 'User'
    
    def features_display(self, obj):
        """Display features in a readable format"""
        if obj.features:
            features_html = []
            for key, value in obj.features.items():
                features_html.append(f"<strong>{key.replace('_', ' ').title()}:</strong> {value}")
            return format_html('<br>'.join(features_html))
        return "No features available"
    features_display.short_description = 'Extracted Features'
    
    def get_queryset(self, request):
        """Optimize queryset for admin listing"""
        qs = super().get_queryset(request)
        return qs.select_related('user').prefetch_related()
    
    def has_change_permission(self, request, obj=None):
        """Only allow viewing, not editing"""
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion only for superusers"""
        return request.user.is_superuser


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin interface for user activity tracking"""
    
    list_display = ('user', 'action', 'ip_address', 'timestamp', 'user_agent_short')
    list_filter = ('action', 'timestamp', 'user__is_staff')
    search_fields = ('user__username', 'action', 'ip_address')
    readonly_fields = ('user', 'action', 'ip_address', 'user_agent', 'details', 'timestamp')
    ordering = ('-timestamp',)
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'action', 'timestamp')
        }),
        ('Technical Details', {
            'fields': ('ip_address', 'user_agent', 'details_display'),
        }),
    )
    
    def user_agent_short(self, obj):
        """Show shortened user agent"""
        if obj.user_agent:
            return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return "Unknown"
    user_agent_short.short_description = 'User Agent'
    
    def details_display(self, obj):
        """Display details in a readable format"""
        if obj.details:
            details_html = []
            for key, value in obj.details.items():
                details_html.append(f"<strong>{key}:</strong> {value}")
            return format_html('<br>'.join(details_html))
        return "No additional details"
    details_display.short_description = 'Additional Details'
    
    def has_add_permission(self, request):
        """Prevent manual addition of activities"""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Activities are read-only"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion only for superusers"""
        return request.user.is_superuser


# Customize admin site headers
admin.site.site_header = "PhishShield Administration"
admin.site.site_title = "PhishShield Admin"
admin.site.index_title = "Welcome to PhishShield Administration"