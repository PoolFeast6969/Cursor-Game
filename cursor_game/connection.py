from omnibus.factories import websocket_connection_factory

game = []

def mousemove_connection_factory(auth_class, pubsub):
    class GeneratedConnection(websocket_connection_factory(auth_class, pubsub)):
        player = []
        def command_subscribe(self, args):
            GeneratedConnection.player = [self.authenticator.get_identifier(),{'username':'fagatron'}]
            if self.subscriber is not None:
                game.append(GeneratedConnection.player)
                self.log('info', u'GAME: {0}'.format('added ' + str(GeneratedConnection.player) + ' to game'))
            return super(GeneratedConnection, self).command_subscribe(args)

        def close_connection(self):
            game.remove(GeneratedConnection.player)
            self.log('info', u'GAME: {0}'.format('removed ' + str(GeneratedConnection.player) + ' from game'))
            self.pubsub.publish(
                'mousemoves', 'disconnect',
                sender=self.authenticator.get_identifier()
            )
            return super(GeneratedConnection, self).close_connection()

    return GeneratedConnection
