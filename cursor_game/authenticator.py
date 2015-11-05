import hashlib
import hmac

from django.conf import settings
from django.utils.encoding import force_bytes
from importlib import import_module
from django.conf import settings

def gameauthenticator_factory():
    """
    `userauthenticator_factory` returns a Authenticator class which does some stuff.
    """
    from .authenticator import GameAuthenticator
    return GameAuthenticator

class GameAuthenticator(object):
    @classmethod
    def authenticate(cls, args):
        # First of all, check if we found an auth_token
        print 'Trying to authenticate'
        if ':' in args:
            try:
                user_id, token = args.split(':')
                SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
                identifier = SessionStore.session_key
                print str(identifier)+str(user_id)
            except ValueError:
                return None

        if not cls.validate_auth_token(identifier, token):
            print 'failed to validate'
            return None

        else:
            # No auth_token, assume anonymous connection.
            identifier = args
            user = None
            print 'anonymous'

        print token
        print identifier
        print user_id

        return cls(identifier, user)

    @classmethod
    def get_auth_token(cls, user_id):
        # Generate an auth token for the user id of a connection.
        print 'generating id'
        return hmac.new(
            force_bytes(settings.SECRET_KEY),
            force_bytes(user_id),
            hashlib.sha1
        ).hexdigest()

    @classmethod
    def validate_auth_token(cls, user_id, token):
        # Compare generated auth token with received auth token.
        print 'comparing token with '+str(user_id)
        generatedtoken = cls.get_auth_token(user_id)
        print 'generated '+generatedtoken
        print 'received '+token
        return generatedtoken == token


    def __init__(self, identifier, user):
        self.identifier = identifier
        self.user = user

    def get_identifier(self):
        return self.identifier

    def can_subscribe(self, channel):
        # If a user is authenticated, subscription is allowed.
        return self.user is not None

    def can_unsubscribe(self, channel):
        # If a user is authenticated, un-subscription is allowed.
        return self.user is not None

    def can_publish(self, channel):
        # If a user is authenticated and is staff member, publishing is allowed.
        return self.user is not None
