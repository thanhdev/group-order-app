from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models import F
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Member(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    picture = models.URLField(blank=True, null=True)


class TransactionManager(models.Manager):
    def create(self, **kwargs):
        from_member: Member = kwargs.pop("from_member")
        to_member: Member = kwargs.pop("to_member")
        amount: float = kwargs.pop("amount")

        with transaction.atomic():
            from_member.balance = F("balance") - amount
            from_member.save()
            to_member.balance = F("balance") + amount
            to_member.save()
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
            for obj in objs:
                obj.from_member.balance = F("balance") - obj.amount
                obj.from_member.save()
                obj.to_member.balance = F("balance") + obj.amount
                obj.to_member.save()

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


@receiver(post_delete, sender=Transaction)
def refund_transaction(sender, instance, **kwargs):
    if instance.from_member == instance.to_member:
        return
    with transaction.atomic():
        instance.from_member.balance = F("balance") + instance.amount
        instance.to_member.balance = F("balance") - instance.amount
        Member.objects.bulk_update(
            [instance.from_member, instance.to_member], ["balance"]
        )
