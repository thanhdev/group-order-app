from mixer.backend.django import mixer
from rest_framework.reverse import reverse_lazy

from core.tests import MemberTestCase
from orders.models import Order


class TestOrderViewSet(MemberTestCase):
    def setUp(self):
        super().setUp()
        mixer.cycle(2).blend(Order, member=self.member, is_paid=True)
        mixer.cycle(3).blend(Order, member=self.member, is_paid=False)
        mixer.cycle(2).blend(Order, member=self.member_2, is_paid=True)

    def test_create(self):
        self.client.force_authenticate(self.member)
        data = {
            "items": [
                {"name": "item 1", "quantity": 1, "unit_price": 100},
                {"name": "item 2", "quantity": 2, "unit_price": 200},
            ]
        }
        response = self.client.post(reverse_lazy("orders-list"), data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data["items"]), 2)

        order = Order.objects.last()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 2)

    def test_list(self):
        self.client.force_authenticate(self.member)
        response = self.client.get(reverse_lazy("orders-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

        # filter by is_paid
        response = self.client.get(
            reverse_lazy("orders-list"), {"is_paid": True}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

        # filter by member
        response = self.client.get(
            reverse_lazy("orders-list"), {"member": self.member_2.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
