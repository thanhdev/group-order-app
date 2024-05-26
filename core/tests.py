from rest_framework.test import APITestCase

from members.models import Member


class MemberTestCase(APITestCase):
    def setUp(self):
        self.member = Member.objects.create_user(
            username="member", email="member@gmail.com", password="test"
        )
        self.member_2 = Member.objects.create_user(
            username="member_2", email="member_2@gmail.com", password="test"
        )
