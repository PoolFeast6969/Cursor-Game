from omnibus.factories import websocket_connection_factory

game = {}

def gamelog(self, message):
    self.log('info', 'GAME: {0}'.format(message))
    self.pubsub.publish('mousemoves', 'chat', {'message':message}, sender='Server')

def player_connection(auth_class, pubsub):
    class GeneratedConnection(websocket_connection_factory(auth_class, pubsub)):
        def __init__(self, *args, **kwargs):
            self.player = {'username':None,'picture':None}
            super(GeneratedConnection, self).__init__(*args, **kwargs)

        def command_subscribe(self, args):
            result = super(GeneratedConnection, self).command_subscribe(args)
            if result is not False:
                self.player['username'] = self.request.host
                self.player['picture'] = 'dunno'
                self.id = self.authenticator.get_identifier()
                game[self.id] = self.player.copy()
                gamelog(self, 'added ' + self.player['username'] + ' to the game')
                self.pubsub.publish('mousemoves', 'update', game, sender='Server')

        def close_connection(self):
            del game[self.id]
            gamelog(self, 'removed ' + self.player['username'] + ' from game')
            self.pubsub.publish('mousemoves', 'update', game, sender='Server')
            return super(GeneratedConnection, self).close_connection()

    return GeneratedConnection
