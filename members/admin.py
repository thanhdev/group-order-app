from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _

from members.models import Member, Transaction


@admin.register(Member)
class MemberAdmin(UserAdmin):
    model = Member
    list_display = ("id", "email", "name", "is_staff")
    search_fields = ("email", "name")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = (
        "id",
        "from_member",
        "to_member",
        "amount",
        "type",
        "created_at",
    )
    search_fields = ("from_member__email", "to_member__email")
    ordering = ("-created_at",)
    list_filter = ("type",)
    readonly_fields = (
        "from_member",
        "to_member",
        "amount",
        "type",
        "created_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "from_member",
                    "to_member",
                    "amount",
                    "type",
                    "created_at",
                )
            },
        ),
    )
