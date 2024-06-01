from mixer.backend.django import mixer
from rest_framework.reverse import reverse_lazy

from core.tests import OrderTestCase
from members.models import Transaction
from orders.enums import GroupOrderStatus, OrderStatus
from orders.models import Order, GroupOrder, OrderItem


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
        self.assertEqual(len(response.data), 9)

        # filter by is_paid
        response = self.client.get(
            reverse_lazy("orders-list"), {"is_paid": True}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

        # filter by member
        response = self.client.get(
            reverse_lazy("orders-list"), {"member": self.member.id}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)

    def test_retrieve(self):
        self.client.force_authenticate(self.member)
        order = self.draft_orders[0]
        mixer.blend(OrderItem, order=order, name="item 1", unit_price=100)
        mixer.blend(
            OrderItem, order=order, name="item 2", unit_price=200, quantity=2
        )
        url = reverse_lazy("orders-detail", kwargs={"pk": order.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["ordered_by"]["id"], self.member.id)
        self.assertEqual(response.data["status"], OrderStatus.DRAFT)
        self.assertEqual(len(response.data["items"]), 2)
        self.assertEqual(response.data["total_cost"], 500)


class TestGroupOrderViewSet(OrderTestCase):
    def test_create(self):
        self.client.force_authenticate(self.member)
        order_ids = [order.id for order in self.draft_orders[:3]]
        data = {"orders": order_ids}
        response = self.client.post(reverse_lazy("group-orders-list"), data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(response.data["orders"]), 3)

        group_order = GroupOrder.objects.last()
        self.assertIsNotNone(group_order)
        self.assertEqual(group_order.host_member, self.member)
        self.assertEqual(group_order.status, GroupOrderStatus.IN_PROGRESS)
        self.assertEqual(group_order.orders.count(), 3)
        for order in group_order.orders.all():
            self.assertEqual(order.status, GroupOrderStatus.IN_PROGRESS)

    def test_list(self):
        self.client.force_authenticate(self.member)
        response = self.client.get(reverse_lazy("group-orders-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        # filter by host_member
        response = self.client.get(
            reverse_lazy("group-orders-list"),
            {"host_member": self.member_2.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["host_member"]["id"], self.member_2.id
        )

        # filter by status
        response = self.client.get(
            reverse_lazy("group-orders-list"),
            {"status": GroupOrderStatus.IN_PROGRESS},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["status"], GroupOrderStatus.IN_PROGRESS
        )

    def test_retrieve(self):
        self.client.force_authenticate(self.member)
        url = reverse_lazy(
            "group-orders-detail", kwargs={"pk": self.group_order.id}
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["host_member"]["id"], self.member.id)
        self.assertEqual(response.data["status"], GroupOrderStatus.IN_PROGRESS)
        self.assertEqual(len(response.data["orders"]), 2)

    def test_delete(self):
        self.client.force_authenticate(self.member)
        url = reverse_lazy(
            "group-orders-detail", kwargs={"pk": self.group_order.id}
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.group_order.refresh_from_db()
        self.assertEqual(self.group_order.status, GroupOrderStatus.CANCELLED)
        self.assertEqual(
            Order.objects.filter(group_order=self.group_order).count(), 0
        )

    def test_complete(self):
        group_order = self.group_order
        url = reverse_lazy(
            "group-orders-complete", kwargs={"pk": group_order.id}
        )
        data = {
            "orders": [self.orders[0].id],
            "actual_amount": 80,
        }

        # not host
        self.client.force_authenticate(self.member_2)
        response = self.client.put(url)
        self.assertEqual(response.status_code, 404)

        # valid
        self.client.force_authenticate(self.member)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], GroupOrderStatus.COMPLETED)
        group_order.refresh_from_db()
        # total cost of order 1: 100, discount: 0.2, actual amount: 80
        self.assertEqual(group_order.actual_amount, 80)
        self.assertEqual(group_order.status, GroupOrderStatus.COMPLETED)

        self.orders[0].refresh_from_db()
        self.assertEqual(self.orders[0].status, OrderStatus.COMPLETED)
        self.orders[1].refresh_from_db()
        self.assertEqual(self.orders[1].status, OrderStatus.CANCELLED)
        self.member.refresh_from_db()
        self.assertEqual(self.member.balance, 80)
        self.member_2.refresh_from_db()
        self.assertEqual(self.member_2.balance, -80)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_complete_self_hosted_order(self):
        group_order = mixer.blend(GroupOrder, host_member=self.member)
        order = mixer.blend(
            Order,
            group_order=group_order,
            member=self.member,
            status=OrderStatus.IN_PROGRESS,
        )
        mixer.blend(OrderItem, order=order, unit_price=100, quantity=1)

        url = reverse_lazy(
            "group-orders-complete", kwargs={"pk": group_order.id}
        )
        data = {
            "orders": [order.id],
            "actual_amount": 80,
        }

        self.client.force_authenticate(self.member)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], GroupOrderStatus.COMPLETED)
        self.member.refresh_from_db()
        self.assertEqual(self.member.balance, 0)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.last()
        self.assertEqual(transaction.amount, 80)
        self.assertEqual(transaction.from_member, self.member)
        self.assertEqual(transaction.to_member, self.member)
        self.assertEqual(transaction.type, Transaction.Type.COMPLETE_ORDER)

    def test_complete_empty_orders(self):
        group_order = self.group_order
        url = reverse_lazy(
            "group-orders-complete", kwargs={"pk": group_order.id}
        )
        data = {
            "orders": [],
            "actual_amount": 0,
        }

        # valid
        self.client.force_authenticate(self.member)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], GroupOrderStatus.COMPLETED)
