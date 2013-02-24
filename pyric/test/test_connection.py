import unittest
import mocks
import pyric.connection as connection

class ConnectionTest(unittest.TestCase):
    ''' Testing the connection '''

    def setUp(self):
        self.socket = mocks.Socket()
        def mockSocket(): 
            return self.socket

        connection.newSocket = mockSocket
        assert connection.newSocket() is self.socket

        self.pyric = mocks.Pyric()
        self.pyric.ipaddr = '10.0.0.1'
        self.pyric.server = 'irc.veiset.org'
        self.pyric.port   = 6667
        self.pyric.nick   = 'vzbot'
        self.pyric.ident  = '~vz'
        self.pyric.name   = 'vz'
    


    def test_that_connection_socket_sends_connection_data(self):
        connection.connect(self.pyric)
        e = self.socket.events
        e.reverse()
        assert e.pop() == ('bind', (self.pyric.ipaddr, self.pyric.port))
        assert e.pop() == ('connect', (self.pyric.server, self.pyric.port))
        assert e.pop() == ('send', bytes('NICK %s\n' % (self.pyric.nick),'UTF-8'))
        assert e.pop() == ('send', bytes('USER %s %s bla :%s\n' 
                            % (self.pyric.ident, self.pyric.server, self.pyric.name),'UTF-8'))

        # ensuring that no more events were recorded
        assert len(self.socket.events) == 0

    def test_that_connection_lives(self):

        self.pyric.connected = True
        self.connection = connection.StayAlive(self.pyric)
        self.connection.receive()
        self.connected = False

    def test_that_disconnect_event_happen_when_thread_completes(self):

        self.pyric.connected = False
        self.connection = connection.StayAlive(self.pyric)
        self.connection.run()

        call, e = self.pyric.events.pop()
        assert call == 'event'
        assert e.get('type') == 'disconnect'

        assert len(self.socket.events) == 0

    def test_that_receive_data_triggers_event(self):
        self.pyric.irc = self.socket
        self.connection = connection.StayAlive(self.pyric)

        self.socket.data = bytes(':vz!~vz@veiset.org PRIVMSG #brbot :hey!\n','UTF-8')
        self.connection.receive()

        call, e = self.pyric.events.pop()
        assert call == 'event'
        assert e.get('type') == 'PRIVMSG'
        assert len(self.socket.events) == 0
    
    def test_that_receive_data_will_not_parse_incomplete_data(self):
        self.pyric.irc = self.socket
        self.connection = connection.StayAlive(self.pyric)

        self.socket.data = bytes(':vz!~vz@veiset.org PRIVMSG #brbot :hey!\n:vz!~vz@vei','UTF-8')
        self.connection.receive()
        assert self.connection.buffr == ':vz!~vz@vei'

        self.socket.data = bytes('set.org PRIVMSG #brbot :hey!\n','UTF-8')
        self.connection.receive()
        assert self.connection.buffr == ''

        
