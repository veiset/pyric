class Log:
    def warn(self,msg): ''' '''
    def error(self,msg): ''' '''
    def info(self,msg): ''' '''

class Socket():

    def __init__(self):
        self.events = []
    
    def connect(self, con):
        self.events.append(('connect', con))

    def bind(self, con):
        self.events.append(('bind', con))

    def send(self, data):
        self.events.append(('send', data))
        

class Pyric:

    def __init__(self):
        self.log = Log()

