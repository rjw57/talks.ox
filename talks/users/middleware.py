import logging
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib import auth

from .models import TalksUser

logger = logging.getLogger(__name__)


class TalksUserMiddleware(object):

    def process_request(self, request):
        if request.user.is_authenticated():
            try:
                request.tuser = request.user.talksuser
            except TalksUser.DoesNotExist:
                # Defensive code here, if our signal to create a TalksUser
                # fails for some reason...
                logger.error("User (%s) has authenticated with no TalksUser"
                             % request.user)
                request.tuser = None
        else:
            request.tuser = None
        # Have to return None so other middlewares are called
        return None


class TestAuthBackend(AuthenticationMiddleware):

    def process_request(self, request):
        if 'autologin' in request.cookies:
            values = request.cookies['autologin']
            username, password = values.split(':')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
        else:
            return
