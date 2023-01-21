from rest_auth.views import PasswordChangeView
from email_service.password_change_email import password_change_email
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from rest_framework.decorators import api_view
from drf_yasg import openapi

from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from users.models import User, UserManager
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import Http404
from subscription.models import Subscription

class PostSuccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        response = super(PostSuccessMixin, self).dispatch(request, *args, **kwargs)
        if response.status_code == 200:
            password_change_email(recipient=request.user.email)
        return response

class CustomPasswordChangeView(PostSuccessMixin, PasswordChangeView):
    pass
    # def post(self, etc):
    #     return Response({"detail": _("New password has been saved.")})
    
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'token': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(['POST'])

def verify_identity_token(request):
    # number = randint(1, 10)
    # response = {'random_number': number}
    # return Response(response)


        # (Receive token by HTTPS POST)
        # ...

    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
        idinfo = id_token.verify_oauth2_token(request.data['token'], requests.Request(), CLIENT_ID)

        # Or, if multiple clients access the backend server:
        # idinfo = id_token.verify_oauth2_token(token, requests.Request())
        # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
        #     raise ValueError('Could not verify audience.')

        # If auth request is from a G Suite domain:
        # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
        #     raise ValueError('Wrong hosted domain.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']
        email = idinfo['email'].lower()
        aud = idinfo['aud']
        given_name = idinfo['given_name']
        family_name = idinfo['family_name']
        print(userid)

        
        try:          
            # if it does, connect this new social login to the existing user
            user = User.objects.get(email=email)

        # if it does not, let allauth take care of this new social account
        except:
            from django.utils.crypto import get_random_string
            p = get_random_string(length=10)
            user = UserManager.create_user(email=email, password=p, first_name=given_name, last_name=family_name)
            Subscription.objects.create_subscription(user)
            user.save()

        
        token, created = Token.objects.get_or_create(user=user)

        # response = {'userid': userid, 'email':email, 'aud': aud, 'key': token.key}
        response = {'key': token.key}

        # return Response({'token': token.key})
        return Response(response)

    except ValueError:
        # Invalid token
        raise Http404("Unable to verify token")
