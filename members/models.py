from django.contrib.auth.models import AbstractUser
from django.db import models, transaction


class Member(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


class TransactionManager(models.Manager):
    def create(self, **kwargs):
        from_member: Member = kwargs.pop("from_member")
        to_member: Member = kwargs.pop("to_member")
        amount: float = kwargs.pop("amount")

        with transaction.atomic():
            from_member.balance -= amount
            to_member.balance += amount
            Member.objects.bulk_update([from_member, to_member], ["balance"])
            return super().create(
                from_member=from_member,
                to_member=to_member,
                amount=amount,
                **kwargs,
            )

    def bulk_create(
        self,
        objs,
        batch_size=None,
        ignore_conflicts=False,
        update_conflicts=False,
        update_fields=None,
        unique_fields=None,
    ):
        with transaction.atomic():
            _members = []
            for obj in objs:
                obj.from_member.balance -= obj.amount
                obj.to_member.balance += obj.amount
                _members.append(obj.from_member)
                _members.append(obj.to_member)
            Member.objects.bulk_update(_members, ["balance"])
            return super().bulk_create(
                objs,
                batch_size=batch_size,
                ignore_conflicts=ignore_conflicts,
                update_conflicts=update_conflicts,
                update_fields=update_fields,
                unique_fields=unique_fields,
            )


class Transaction(models.Model):
    objects = TransactionManager()

    class Type(models.TextChoices):
        TRANSFER = "transfer", "Transfer"
        COMPLETE_ORDER = "complete_order", "Complete Order"

    from_member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="sent_transactions",
    )
    to_member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="received_transactions",
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=50, choices=Type.choices, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
