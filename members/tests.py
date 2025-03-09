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
    def setUp(self):
        super().setUp()
        mixer.cycle().blend(Transaction, from_member=self.member)
        mixer.cycle().blend(Transaction, to_member=self.member)

    def test_list(self):
        self.client.force_authenticate(self.member)
        response = self.client.get(reverse_lazy("transactions-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

        # Filter by member
        response = self.client.get(
            reverse_lazy("transactions-list"), {"member": self.member.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 10)

        # Filter by from_member
        response = self.client.get(
            reverse_lazy("transactions-list"), {"from_member": self.member.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_create(self):
        self.client.force_authenticate(self.member)
        data = {"to_member": self.member_2.id, "amount": -100}

        # Invalid amount
        response = self.client.post(reverse_lazy("transactions-list"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["amount"], ["Invalid amount."])

        # Successful transfer
        data["amount"] = 100
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


class TestMemberProfileView(MemberTestCase):
    url = reverse_lazy("members-me")

    def test_get(self):
        self.client.force_authenticate(self.member)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.member.id)
        self.assertEqual(response.data["email"], self.member.email)
        self.assertEqual(response.data["name"], self.member.name)
        self.assertEqual(response.data["balance"], "0.00")

    def test_patch(self):
        self.client.force_authenticate(self.member)
        data = {"name": "new name", "picture": "https://new-picture.com"}
        response = self.client.patch(self.url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.member.id)
        self.assertEqual(response.data["email"], self.member.email)
        self.assertEqual(response.data["name"], "new name")
        self.assertEqual(response.data["picture"], "https://new-picture.com")
        self.assertEqual(response.data["balance"], "0.00")
