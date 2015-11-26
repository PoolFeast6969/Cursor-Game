from django.conf import settings
import cursor_game.authenticator
from django.core.cache import cache

def game(request):
    """
    `game` context processor provides auth token
    """

    print "user has "+str(request.session.session_key)

    auth_class = eval(settings.OMNIBUS_AUTHENTICATOR_FACTORY)()
    auth_token = auth_class.get_auth_token(request.session.get(sessionid))

    return {
        'GAME_AUTH_TOKEN': auth_token
    }
