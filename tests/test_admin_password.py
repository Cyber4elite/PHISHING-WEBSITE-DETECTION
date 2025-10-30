#!/usr/bin/env python
"""Test script to check password display functionality"""

import os
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'phishshield.settings')

import django
django.setup()

from django.contrib.auth.models import User
from scanner.admin import CustomUserAdmin

def test_password_display():
    """Test the password_display method"""
    try:
        # Get a user
        user = User.objects.first()
        if not user:
            print("No users found in database")
            return
        
        # Create admin instance
        admin = CustomUserAdmin(User, None)
        
        # Test password display
        password_display = admin.password_display(user)
        print(f"User: {user.username}")
        print(f"Password field: {user.password}")
        print(f"Password display result: {password_display}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_password_display()
