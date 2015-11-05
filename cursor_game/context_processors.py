from django.conf import settings

def game(request):
    """
    `game` context processor provides auth token
    """

    auth_token = settings.OMNIBUS_AUTHENTICATOR_FACTORY.get_auth_token(request.session.session_key)

    return {
        'GAME_AUTH_TOKEN': auth_token
    }
