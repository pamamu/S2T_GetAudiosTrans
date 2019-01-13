import abc
import Pyro4


@Pyro4.expose
class ContainerHandler(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, container_name, main_uri):
        """
        TODO DOCUMENTATION
        :param container_name:
        """
        self.container_name = container_name
        self.daemon = Pyro4.Daemon()
        self.uri = str(self.daemon.register(self, objectId=self.container_name))
        self.main_server = Pyro4.Proxy(main_uri)
        self.running = False
        print("Container {}: Created".format(self.container_name))

    def register(self):
        self.main_server.register(self.container_name, self.uri)
        print("Container {}: Registered".format(self.container_name))

    def start(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        print("Container {}: Started".format(self.container_name))
        self.daemon.requestLoop()

    @abc.abstractmethod
    def run(self, **kwargs):
        """
        TODO DOCUMENTATION
        :param kwargs:
        :return:
        """
        raise NotImplementedError

    def stop(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        self.daemon.close()
        self.main_server.unregister(self.container_name)
        print("Container {}: Stopped".format(self.container_name))

    @abc.abstractmethod
    def info(self):
        """
        TODO DOCUMENTATION
        :return:
        """
        raise NotImplementedError
