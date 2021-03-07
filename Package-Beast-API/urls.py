"""Package-Beast-API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework import routers
from arrangements import views
from rest_framework_swagger.views import get_swagger_view
from django.urls import include
from django.views.generic.base import RedirectView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth.views import PasswordResetView
from rest_auth.registration.views import VerifyEmailView
from .views import CustomPasswordChangeView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

schema_view = get_schema_view(
    openapi.Info(
        title="Package Beast API",
        default_version='v1',
        description="A simple API for packaging optimization and payments",
        #   terms_of_service="Terms of use",
        #   contact=openapi.Contact(email="No Problems"),
        license=openapi.License(
            name="Copyright - Package Beast. All rights reserved"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)


# router = routers.DefaultRouter()
# router.register(r'users', views.UserList)
# router.register(r'arrangements', views.ArrangementList)
# router.register(r'groups', views.GroupViewSet)

urlpatterns = [

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    # allows login and logout from endpoint, eg. /arrangments
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('arrangements.urls')),
    path('', include('containers.urls')),
    path('', include('items.urls')),
    path('', include('users.urls')),
    path('', include('payment.urls')),
    path('accounts/password/change/', CustomPasswordChangeView.as_view()),
    path('accounts/', include('rest_auth.urls')),
    path('accounts/registration/', include('rest_auth.registration.urls')),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(
        r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetView, name='password_reset_confirm'),
    re_path(r'^.*$', RedirectView.as_view(url='/accounts/login/', permanent=False)),

]
