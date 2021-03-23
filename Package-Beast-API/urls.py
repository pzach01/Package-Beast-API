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
from subscription.models import Subscription
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
import os

from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """

        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        sociallogin.connect(request, user)
    def save_user(self, request, sociallogin, form=None):
        user = super(CustomSocialAccountAdapter, self).save_user(request, sociallogin, form)
        Subscription.objects.create_subscription(user)
        return user

class SchemaGenerator(OpenAPISchemaGenerator):
  def get_schema(self, request=None, public=False):
    schema = super(SchemaGenerator, self).get_schema(request, public)
    schema.basePath = os.getenv('API_ROOT_URL')
    return schema


# a = os.getenv('API_ROOT_URL')
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
    # url=a, # Important bit
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
    path('', include('shipments.urls')),
    path('', include('quotes.urls')),
    path('', include('users.urls')),
    path('', include('payment.urls')),
    path('', include('addresses.urls')),
    path('accounts/password/change/', CustomPasswordChangeView.as_view()),
    path('accounts/', include('rest_auth.urls')),
    path('accounts/registration/', include('rest_auth.registration.urls')),
    path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    url(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),
    re_path(
        r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', PasswordResetView, name='password_reset_confirm'),
    re_path(r'^.*$', RedirectView.as_view(url='/accounts/login/', permanent=False)),

]
