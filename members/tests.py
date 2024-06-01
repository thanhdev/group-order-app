from mixer.backend.django import mixer
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from core.tests import MemberTestCase
from members.models import Member, Transaction


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


class TestTransactionViewSet(MemberTestCase):
    def test_list(self):
        self.client.force_authenticate(self.member)
        mixer.cycle().blend(Transaction)
        response = self.client.get(reverse_lazy("transactions-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_create(self):
        self.client.force_authenticate(self.member)
        data = {"to_member": self.member_2.id, "amount": 100}

        # Insufficient balance
        response = self.client.post(reverse_lazy("transactions-list"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["amount"], ["Insufficient balance"])

        # Successful transfer
        self.member.balance = 1000
        self.member.save()
        response = self.client.post(reverse_lazy("transactions-list"), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["from_member"]["id"], self.member.id)
        self.assertEqual(response.data["to_member"]["id"], self.member_2.id)
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["type"], Transaction.Type.TRANSFER)

        self.member.refresh_from_db()
        self.assertEqual(self.member.balance, 900)
        self.member_2.refresh_from_db()
        self.assertEqual(self.member_2.balance, 100)


class TestTokenObtainPairView(MemberTestCase):
    def test_login(self):
        data = {"email": self.member.email, "password": "test"}
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
        data = {"email": self.member.email, "password": "wrong"}
        response = self.client.post(reverse_lazy("token_obtain_pair"), data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data["detail"],
            "No active account found with the given credentials",
        )
