"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from members.views import (
    MemberViewSet,
    TransactionViewSet,
    MemberMeView,
    login,
    logout,
    callback,
)
from orders.views import OrderViewSet, GroupOrderViewSet, GroupViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"members", MemberViewSet, basename="members")
router.register(r"groups", GroupViewSet, basename="groups")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"group-orders", GroupOrderViewSet, basename="group-orders")
router.register(r"transactions", TransactionViewSet, basename="transactions")

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth0
    path("auth0/login", login, name="oauth0-login"),
    path("auth0/logout", logout, name="oauth0-logout"),
    path("auth0/callback", callback, name="oauth0-callback"),
    # Docs
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # APIs
    path(
        "api/members/me",
        MemberMeView.as_view(),
        name="members-me",
    ),
    path("api/", include(router.urls)),
]

urlpatterns += [
    re_path(
        r"^.*$",
        TemplateView.as_view(template_name="index.csr.html"),
        name="index",
    ),
]
