from omnibus.factories import websocket_connection_factory

game = []

def gamelog(self, message):
    message = 'GAME: {0}'.format(message)
    self.log('info', message)
    self.pubsub.publish('mousemoves', 'chat', {'message':message}, sender='server')

def player_connection(auth_class, pubsub):
    class GeneratedConnection(websocket_connection_factory(auth_class, pubsub)):
        def __init__(self, *args, **kwargs):
            self.player = {'id':None,'username':None}
            super(GeneratedConnection, self).__init__(*args, **kwargs)

        def command_subscribe(self, args):
            result = super(GeneratedConnection, self).command_subscribe(args)
            if result is not False:
                self.player['id'] = self.authenticator.get_identifier()
                self.player['username'] = self.request.host
                game.append(self.player.copy())
                gamelog(self, 'added ' + self.player['username'] + ' to the game')
                self.pubsub.publish('mousemoves', 'update', dict(enumerate(game)), sender='server')

        def close_connection(self):
            game.remove(self.player)
            gamelog(self, 'removed ' + self.player['username'] + ' from game')
            self.pubsub.publish('mousemoves', 'update', dict(enumerate(game)), sender='server')
            return super(GeneratedConnection, self).close_connection()

    return GeneratedConnection
