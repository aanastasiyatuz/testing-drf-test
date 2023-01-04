# https://www.django-rest-framework.org/api-guide/testing/

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterUserView
from .models import User


class AuthTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        User.objects.create_user(email='test@gmail.com', password='12345678')

    def test_register(self):
        data = {
            'email': 'new_user@gmail.com',
            'password': '12345678',
            'password_confirm': '12345678'
            }
        request = self.factory.post('/account/register/', data, format='json')
        view = RegisterUserView.as_view()
        response = view(request)

        assert response.status_code == 201
        assert User.objects.filter(email=data['email']).exists()

    def test_login(self):
        data = {
            'email': 'test@gmail.com',
            'password': '12345678'
            }
        request = self.factory.post('/account/token/', data, format='json')
        view = TokenObtainPairView.as_view()
        response = view(request)

        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data
