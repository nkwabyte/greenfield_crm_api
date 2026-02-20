from rest_framework import serializers
from accounts.models import User, EmployeeProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']

class EmployeeProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            'id', 'name', 'role_title', 'salary', 'start_date', 'status', 
            'is_verified', 'created_at', 'updated_at', 'is_deleted',
            'user', 'user_email', 'user_role'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_email', 'user_role']
