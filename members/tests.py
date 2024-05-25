from django.contrib.auth.models import User
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase


class TestMemberViewSet(APITestCase):
    def test_create(self):
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(reverse_lazy('members-list'), data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['username'], data['username'])
        self.assertTrue('password' not in response.data)

        user = User.objects.get(username='test')
        self.assertTrue(user.check_password('test'))
        self.assertTrue(user.is_active)


class TestTokenObtainPairView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')

    def test_login(self):
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(reverse_lazy('token_obtain_pair'), data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

        access = response.data['access']
        response = self.client.get(reverse_lazy('members-me'), HTTP_AUTHORIZATION=f'Bearer {access}')
        self.assertEqual(response.status_code, 200)

    def test_login_invalid(self):
        data = {
            'username': 'test',
            'password': 'invalid'
        }
        response = self.client.post(reverse_lazy('token_obtain_pair'), data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')
