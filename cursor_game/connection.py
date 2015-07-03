from omnibus.factories import websocket_connection_factory

game = []

def gamelog(self, message):
    message = 'GAME: {0}'.format(message)
    self.log('info', message)
    self.pubsub.publish('mousemoves', 'chat', {None:message}, sender='server')

def player_connection(auth_class, pubsub):
    class GeneratedConnection(websocket_connection_factory(auth_class, pubsub)):
        player = {'id':None,'username':None}
        def command_subscribe(self, args):
            result = super(GeneratedConnection, self).command_subscribe(args)
            if result is not False:
                GeneratedConnection.player['id'] = self.authenticator.get_identifier()
                GeneratedConnection.player['username'] = self.request.host
                game.append(GeneratedConnection.player.copy())
                gamelog(self, 'added ' + GeneratedConnection.player['username'] + ' to game')
                self.pubsub.publish('mousemoves', 'connect', dict(enumerate(game)), sender='server')

        def close_connection(self):
            game.remove(GeneratedConnection.player)
            gamelog(self, 'removed ' + GeneratedConnection.player['username'] + ' from game')
            self.pubsub.publish('mousemoves', 'disconnect', dict(enumerate(game)), sender='server')
            return super(GeneratedConnection, self).close_connection()

    return GeneratedConnection
