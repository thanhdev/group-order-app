from mixer.backend.django import mixer
from rest_framework.test import APITestCase

from members.models import Member
from orders.enums import OrderStatus, GroupOrderStatus
from orders.models import Order, GroupOrder


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
        self.group_order = mixer.blend(GroupOrder, host_member=self.member)
        self.completed_orders = mixer.cycle(2).blend(
            Order,
            member=self.member,
            status=OrderStatus.COMPLETED,
            group_order=self.group_order,
        )
        self.draft_orders = mixer.cycle(3).blend(Order, member=self.member)

        mixer.cycle(2).blend(Order, member=self.member_2, is_paid=True)
        mixer.blend(
            GroupOrder,
            host_member=self.member_2,
            status=GroupOrderStatus.COMPLETED,
        )
