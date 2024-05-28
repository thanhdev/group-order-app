# Generated by Django 4.2.13 on 2024-05-28 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("orders", "0002_alter_grouporder_status_alter_order_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grouporder",
            name="actual_amount",
            field=models.DecimalField(
                blank=True,
                decimal_places=2,
                editable=False,
                max_digits=10,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="grouporder",
            name="host_member",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="hosted_group_orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="grouporder",
            name="status",
            field=models.CharField(
                choices=[
                    ("in_progress", "In Progress"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="in_progress",
                editable=False,
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="group_order",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="orders",
                to="orders.grouporder",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="is_paid",
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name="order",
            name="member",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="orders",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("in_progress", "In Progress"),
                    ("completed", "Completed"),
                    ("cancelled", "Cancelled"),
                ],
                default="draft",
                editable=False,
                max_length=50,
            ),
        ),
    ]
