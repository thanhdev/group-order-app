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
