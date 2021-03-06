import textwrap
import pyric.connection as connection
import socket


class Logger():
    def info(self, msg):
        print('.', msg)

    def warn(self, msg):
        print('+', msg)

    def error(self, msg):
        print('!', msg)


class Instance():

    WILDCARD = "*"

    def __init__(self, nick, ident, name, server, port, ipaddr=None):
        '''
        Construct a connection ready to connect to an IRC server.

        Keyword arguments:
        nick     -- the bot nickname
        ident    -- the bot ident
        name     -- the bot real name
        server   -- irc server to connect to
        port     -- irc server port
        ipaddr   -- ipaddress to bind a host against (vhost)
        '''
        self.nick = nick
        self.ident = ident
        self.name = name
        self.server = server
        self.port = port
        self.ipaddr = ipaddr
        self.connection = None
        self.connected = False
        self.log = Logger()
        self.listeners = {}

    def addListener(self, event, function):
        self.log.info(('addListener', event, function))
        if event in self.listeners:
            self.listeners[event].append(function)
        else:
            self.listeners[event] = [function]

    def removeListener(self, event, function):
        self.log.info(('removeListener', event, function))
        if function in self.listeners[event]:
            self.listeners[event].remove(function)

    def event(self, e):
        if self.WILDCARD in self.listeners:
            for function in self.listeners[self.WILDCARD]:
                function(e)

        self.log.info(("event", e.get('type'), e.data))
        event = str(e.get('type')).lower()

        if event == "ping":
            self.send('PONG %s' % e.get('msg'))
            self.log.info(("PONG"))

        if event in self.listeners:
            for function in self.listeners[event]:
                function(e)

        if event == "privmsg" and e.get('msg')[0] == '.':
            if len(e.get('msg')) > 1:
                params = e.get('msg').split(' ', 1)
                if len(params) > 1:
                    e.add('param', params[1])
                e.add('cmd', params[0])
                cmd = 'cmd' + params[0]
                e.add('type', cmd)

                self.log.info(("event", e.get('type'), e.data))

                if cmd in self.listeners:
                    for function in self.listeners[cmd]:
                        function(e)

    def connect(self):
        ''' '''
        self.irc = socket.socket()
        connection.connect(self)
        self.connected = True
        self.connection = connection.StayAlive(self)
        self.connection.start()

    def disconnect(self):
        ''' '''
        self.connected = False
        try:
            self.send('QUIT')
        except:
            self.log.warn('Could not communicate with IRC socket')
        try:
            self.irc.close()
        except:
            self.log.warn('Could not close the IRC socket. '
                          '(Might already be closed)')

        self.log.info('Bot terminated')

    def send(self, data):
        self.irc.send(bytes(data + '\r\n', 'UTF-8'))

    def join(self, channel, pswd=None):
        self.send('JOIN %s' % channel)

    def part(self, channel, message=None):
        self.send('PART %s' % channel)

    def mode(self, channel, mode):
        '''
        IRC Channel MODE

        Keyword arguments:
        channel -- IRC channel name
        mode    -- mode (e.g: +o vz)
        '''
        self.send('MODE %s %s' % (channel, mode))

    def say(self, target, message):
        '''
        say() -> None

        Send a message to a target on the connected IRC server.

        Keyword arguments:
        target  -- recipient of given message
        message -- message to send

        From RFC 1459:
          IRC messages are always lines of characters terminated with a CR-LF
          (Carriage Return - Line Feed) pair, and these messages shall not
          exceed 512 characters in length, counting all characters including
          the trailing CR-LF. Thus, there are 510 characters maximum allowed
          for the command and its parameters.

        :nick!ident@host PRIVMSG target :text

        That is: 9 additional chars (:!@<space><space><space>:) and RC-LF
        TODO: 80 is temporary. Should be the length of the bots host.
        '''

        noise = len(self.nick) + len(self.ident) + 80 + len(target) + 9

        lines = textwrap.wrap(message, 512-noise)
        for line in lines:
            self.send('PRIVMSG %s :%s' % (target, line))
