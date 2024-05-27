from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from members.models import Member
from orders.models import Order


class MemberTestCase(APITestCase):
    def setUp(self):
        self.member = Member.objects.create_user(
            username="member", email="member@gmail.com", password="test"
        )
        self.member_2 = Member.objects.create_user(
            username="member_2", email="member_2@gmail.com", password="test"
        )


class OrderTestCase(MemberTestCase):
    def setUp(self):
        super().setUp()
        mixer.cycle(2).blend(Order, member=self.member, is_paid=True)
        self.unpaid_orders = mixer.cycle(3).blend(
            Order, member=self.member, is_paid=False
        )
        mixer.cycle(2).blend(Order, member=self.member_2, is_paid=True)
