from django.apps import AppConfig
from multiprocessing import Process
from django.core.management import call_command
class omnibusAppConfig(AppConfig):
    name = 'omnibus'
    verbose_name = "Start Sever"
    def ready(self):
        if hasattr(self, 'executed'):
            print('eyyyy')
        self.executed = True
        def startserver(self):
            call_command('omnibusd')
        self.socketserver = Process(target = startserver, args = (self,))
        self.socketserver.start()
