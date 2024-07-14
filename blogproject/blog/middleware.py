# blog/middleware.py

import jwt
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import MiddlewareNotUsed
from rest_framework.exceptions import AuthenticationFailed
from .models import Profile

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = [reverse('login'), reverse('register')]  # Adjust with your actual login/register URLs

    def __call__(self, request):
        if request.path in self.excluded_paths:
            return self.get_response(request)

        token = request.COOKIES.get('jwtoken')

        if not token:
            request.user = None
            return self.get_response(request)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print("pl",payload)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        if user is None:
            raise AuthenticationFailed('Unauthenticated!')

        request.user = user
        profile = Profile.objects.filter(user=user).first()
        request.profile = profile
        print("from mw1", request.user.id)
        response = self.get_response(request)
        return response
