from mixer.backend.django import mixer
from rest_framework.reverse import reverse_lazy

from core.tests import OrderTestCase
from orders.enums import GroupOrderStatus
from orders.models import Order, GroupOrder


class TestOrderViewSet(OrderTestCase):
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

    def test_pay(self):
        self.client.force_authenticate(self.member)
        order = self.unpaid_orders[0]
        url = reverse_lazy("orders-pay", kwargs={"pk": order.id})

        # not ready for payment
        response = self.client.put(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["detail"], "This order is not ready for payment."
        )

        # ready
        order.group_order = mixer.blend(
            GroupOrder,
            host_member=self.member,
            status=GroupOrderStatus.IN_PROGRESS,
        )
        order.save()
        response = self.client.put(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_paid"])

        # not host
        order.group_order.host_member = self.member_2
        order.group_order.save()
        response = self.client.put(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.data["detail"],
            "You do not have permission to pay for this order.",
        )


class TestGroupOrderViewSet(OrderTestCase):
    def test_create(self):
        self.client.force_authenticate(self.member)
        order_ids = [order.id for order in self.unpaid_orders[:3]]
        data = {"orders": order_ids}
        response = self.client.post(reverse_lazy("group-orders-list"), data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data["orders"]), 3)

        group_order = GroupOrder.objects.last()
        self.assertIsNotNone(group_order)
        self.assertEqual(group_order.orders.count(), 3)
        self.assertEqual(group_order.host_member, self.member)

    def test_list(self):
        self.client.force_authenticate(self.member)
        response = self.client.get(reverse_lazy("group-orders-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)
