import hashlib
import hmac

from django.conf import settings
from django.utils.encoding import force_bytes

def userauthenticator_factory():
    """
    `userauthenticator_factory` returns a Authenticator class which verifies
    that the connections belongs to a registered user.
    """
    from .authenticator import GameAuthenticator
    return GameAuthenticator

class GameAuthenticator(object):
    @classmethod
    def authenticate(cls, args):
        if ':' in args:
            try:
                identifier, user_id, token = args.split(':')
            except ValueError:
                return None

            if not cls.validate_auth_token(user_id, token):
                return None

            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
            except ImportError:
                from django.contrib.auth.models import User

            try:
                user = User.objects.get(pk=int(user_id), is_active=True)
            except (ValueError, User.DoesNotExist):
                return None
        else:
            identifier = args
            user = None

        return cls(identifier, user)

    @classmethod
    def get_auth_token(cls, user_id):
        return hmac.new(
            force_bytes(settings.SECRET_KEY),
            force_bytes(user_id),
            hashlib.sha1
        ).hexdigest()

    @classmethod
    def validate_auth_token(cls, user_id, token):
        return cls.get_auth_token(user_id) == token

    def __init__(self, identifier, user):
        self.identifier = identifier
        self.user = user

    def get_identifier(self):
        return self.identifier

    def can_subscribe(self, channel):
        return self.user is not None

    def can_unsubscribe(self, channel):
        return self.user is not None

    def can_publish(self, channel):
        return self.user is not None
