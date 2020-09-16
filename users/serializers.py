from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from arrangements.models import Arrangement
from users.models import User
from django.utils.translation import ugettext_lazy as _
import requests
from requests import post
from subscription.models import Subscription
import json
class LoginSerializer(RestAuthLoginSerializer):
    username = None

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    password1 = serializers.CharField(required=True, write_only=True, min_length=8)
    password2 = serializers.CharField(required=True, write_only=True, min_length=8)
    recaptcha_token=serializers.CharField(required=True,write_only=True,max_length=1012)
    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        '''
        secret	Required. The shared key between your site and reCAPTCHA.
        response	Required. The user response token provided by the reCAPTCHA client-side integration on your site.
        remoteip	Optional. The user's IP address.
        '''
        recaptchaInput={
        'secret':'6LfXg8wZAAAAAP3qHCkfmqe3i2DE4EVa72jWDPTK',
        'response':data['recaptcha_token']
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=recaptchaInput)
        resp = json.dumps(resp)
        if resp['score']<1:

            raise serializers.ValidationError(
                _("You were identified as a bot. Please try again or contact technical support.Recaptcha score:"+str(resp['score'])))


        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])


        user.save()
        Subscription.objects.create_subscription(user)

        return user


class UserSerializer(serializers.ModelSerializer):
    arrangements = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'arrangements', 'units', 'dateTimeFormat', 'multiBinPack', 'disableFillContainerAnimation', 'disablePreviousNextItemAnimation', 'animationSpeed']
        read_only_fields = ['arrangements', 'email']