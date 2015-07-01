from omnibus.factories import websocket_connection_factory
from django.http import HttpResponse, HttpRequest

game = []

def player_connection(auth_class, pubsub):
    class GeneratedConnection(websocket_connection_factory(auth_class, pubsub)):
        player = {'id':None,'username':None}
        def command_subscribe(self, args):
            if self.subscriber is not None:
                GeneratedConnection.player['id'] = self.authenticator.get_identifier()
                GeneratedConnection.player['username'] = self.request.host
                game.append(GeneratedConnection.player)
                self.log('info', u'GAME: {0}'.format('added ' + GeneratedConnection.player['username'] + ' to game'))
            return super(GeneratedConnection, self).command_subscribe(args)

        def close_connection(self):
            game.remove(GeneratedConnection.player)
            self.log('info', u'GAME: {0}'.format('removed ' + GeneratedConnection.player['username'] + ' from game'))
            self.pubsub.publish('mousemoves', 'disconnect', sender=self.authenticator.get_identifier())
            return super(GeneratedConnection, self).close_connection()

    return GeneratedConnection
