import socket
import events
import threading

def connect(pyric):
    '''
    Connects to an IRC server.

    Keyword arguments:
    pyric -- an instantiated pyric object
    '''
    irc = socket.socket()

    # Trying to bind vhost
    if pyric.ipaddr:
        try: 
            irc.bind((pyric.ipaddr, pyric.port))
            pyric.log.info("bound IP-address: %s " % pyric.ipaddr)
        except: 
            pyric.log.warn("could not bind IP-address: %s " % pyric.ipaddr)
    
    irc.connect((pyric.server, pyric.port))
    irc.send(bytes('NICK %s\n' % (pyric.nick), 'UTF-8'))
    irc.send(bytes('USER %s %s bla :%s\n' % 
            (pyric.ident, pyric.server, pyric.name), 'UTF-8'))

    return irc


class StayAlive(threading.Thread):

    def __init__(self, pyric):
        '''
        Construct a thread to run in the background to keep the bot alive.

        Keyword arguments:
        pyric -- an instantiated pyric object
        '''
        threading.Thread.__init__(self)
        self.pyric = pyric

    def run(self):
        buffr = ''

        while self.pyric.connected:
            try:
                buffr += str(self.pyric.irc.recv(1024),'UTF-8')
            except:
                self.pyric.log.error(("parse-error",
                    "could not parse data from irc server"))
            data = buffr.split('\n')
            buffr = data.pop()
        
            for line in data:
                line = line.rstrip()
            
                self.pyric.event('_raw', line)

                event, info = events.parse(line)
                self.pyric.event(event, info)

        self.pyric.event('disconnect')
