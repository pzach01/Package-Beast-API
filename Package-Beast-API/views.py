from rest_auth.views import PasswordChangeView
from email_service.password_change_email import password_change_email
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _

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
    