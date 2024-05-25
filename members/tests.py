from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from members.models import Member


class TestMemberViewSet(APITestCase):
    def test_create(self):
        data = {"name": "test", "email": "test@gmail.com", "password": "test"}
        response = self.client.post(reverse_lazy("members-list"), data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["email"], data["email"])
        self.assertTrue("password" not in response.data)

        user = Member.objects.get(email="test@gmail.com")
        self.assertTrue(user.check_password("test"))
        self.assertTrue(user.is_active)


class TestTokenObtainPairView(APITestCase):
    def setUp(self):
        Member.objects.create_user(
            username="test", email="test@gmail.com", password="test"
        )

    def test_login(self):
        data = {"email": "test@gmail.com", "password": "test"}
        response = self.client.post(reverse_lazy("token_obtain_pair"), data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

        access = response.data["access"]
        response = self.client.get(
            reverse_lazy("members-me"), HTTP_AUTHORIZATION=f"Bearer {access}"
        )
        self.assertEqual(response.status_code, 200)

    def test_login_invalid(self):
        data = {"email": "test@gmail.com", "password": "wrong"}
        response = self.client.post(reverse_lazy("token_obtain_pair"), data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )
