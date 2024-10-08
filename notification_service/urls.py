"""
URL configuration for notification_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
    openapi.Info(
        title="Notification Microservice Inc.",
        default_version="v1",
        description="All the endpoints created for Notification Microservice",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),

    path("api/", include("email_service.urls")),
    path("api/", include("push_notifications.urls")),
    path("api/", include("sms_service.urls")),
    path("api/common/", include("common.urls")),
]
