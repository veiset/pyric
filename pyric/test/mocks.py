class Log:
    def warn(self,msg): ''' '''
    def error(self,msg): ''' '''
    def info(self,msg): ''' '''

class Socket():

    def __init__(self):
        self.events = []
        self.data = ''
    
    def connect(self, con):
        self.events.append(('connect', con))

    def bind(self, con):
        self.events.append(('bind', con))

    def send(self, data):
        self.events.append(('send', data))

    def recv(self, n):
        return self.data
        

class Pyric:

    def __init__(self):
        self.log = Log()
        self.events = []

    def event(self, e):
        self.events.append(('event', e))
