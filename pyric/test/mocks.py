def eventMethod1(event):
    return event
def eventMethod2(event):
    return event

def throwMethod(param=None):
    raise Exception

class EventClass():
    def __init__(self):
        self.events = []

    def method(self, event):
        self.events.append(('method', event))

class Log:
    def __init__(self):
        self.events = []

    def warn(self,msg):
        self.events.append(('warn', msg))
    def error(self,msg):
        self.events.append(('error', msg))
    def info(self,msg):
        self.events.append(('info', msg))

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
        
    def close(self):
        self.events.append(('close'))

class Pyric:

    def __init__(self):
        self.events = []
        self.log = Log()

    def event(self, e):
        self.events.append(('event', e))
