import socket
import threading

from ircparser.ircparser import parse
from pyric.events import Event

def connect(pyric):
    '''
    Connects to an IRC server.

    Keyword arguments:
    pyric -- an instantiated pyric object
    '''
    # Try to bind vhost
    if pyric.ipaddr:
        try: 
            pyric.irc.bind((pyric.ipaddr, pyric.port))
            pyric.log.info("bound IP-address: %s " % pyric.ipaddr)
        except: 
            pyric.log.warn("could not bind IP-address: %s " % pyric.ipaddr)
    
    pyric.irc.connect((pyric.server, pyric.port))
    pyric.irc.send(bytes('NICK %s\n' % (pyric.nick), 'UTF-8'))
    pyric.irc.send(bytes('USER %s %s bla :%s\n' % 
            (pyric.ident, pyric.server, pyric.name), 'UTF-8'))


class StayAlive(threading.Thread):

    def __init__(self, pyric):
        '''
        Construct a thread to run in the background to keep the bot alive.

        Keyword arguments:
        pyric -- an instantiated pyric object
        '''
        threading.Thread.__init__(self)
        self.pyric = pyric
        self.buffr = ''

    def run(self):
        ''' Receiving data from IRC socket '''

        while self.pyric.connected:
            self.receive()

        self.pyric.event(Event({'type' : 'disconnect'}))

    def receive(self):
        '''
        Retrieves and parses incoming socket data. Invokes the event callback 
        of the pyric object, pyric.event(e), when new events are received.
        '''

        try:
            self.buffr += str(self.pyric.irc.recv(2048),'UTF-8')
        except:
            self.pyric.log.error(("parse-error", "could not read data correctly from irc server"))

        data = self.buffr.split('\n')
        # data which is not terminated by newline will be kept in buffer
        self.buffr = data.pop()
    
        for line in data:
            try:
                eventdata = parse(line.rstrip(),'dict')
                e = Event(eventdata)
                self.pyric.event(e)
            except:
                self.pyric.log.error(("parse-error", "could not parse received data correctly"))
