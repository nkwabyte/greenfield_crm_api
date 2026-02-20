import jwt
from django.conf import settings
from rest_framework import authentication
from rest_framework import exceptions
from accounts.models import User

class SupabaseJWTAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication class that validates Supabase JWTs.
    """
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        secret = settings.SUPABASE_JWT_SECRET

        if not secret:
            raise exceptions.AuthenticationFailed('Server misconfiguration: missing Supabase JWT secret.')

        try:
            payload = jwt.decode(
                token,
                secret,
                algorithms=["HS256"],
                options={"verify_aud": False}
            )
            
            user_id = payload.get('sub')
            email = payload.get('email', '')
            
            if not user_id:
                raise exceptions.AuthenticationFailed('User ID not found in JWT')
            
            # Use 'sub' as username as it's the unique Supabase UUID
            user, _ = User.objects.get_or_create(
                username=user_id,
                defaults={'email': email, 'is_active': True}
            )
            
            return (user, payload)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token has expired.')
        except jwt.InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f'Invalid token: {str(e)}')
