import unittest
import pyric.connection as connection
import pyric.test.mocks as mocks

class ConnectionTest(unittest.TestCase):
    ''' Testing the connection '''

    def setUp(self):

        self.pyric = mocks.Pyric()
        self.pyric.ipaddr = '10.0.0.1'
        self.pyric.server = 'irc.veiset.org'
        self.pyric.port   = 6667
        self.pyric.nick   = 'vzbot'
        self.pyric.ident  = '~vz'
        self.pyric.name   = 'vz'

        self.irc = mocks.Socket()
        self.pyric.irc = self.irc
    


    def test_that_connection_socket_sends_connection_data(self):
        connection.connect(self.pyric)

        e = self.irc.events
        e.reverse()

        assert e.pop() == ('bind', (self.pyric.ipaddr, self.pyric.port))
        assert e.pop() == ('connect', (self.pyric.server, self.pyric.port))
        assert e.pop() == ('send', bytes('NICK %s\n' % (self.pyric.nick),'UTF-8'))
        assert e.pop() == ('send', bytes('USER %s %s bla :%s\n' 
                            % (self.pyric.ident, self.pyric.server, self.pyric.name),'UTF-8'))

        # ensuring that no more events were recorded
        assert len(self.irc.events) == 0

    def test_that_connection_lives_after_calling_receive_with_no_new_data(self):

        self.pyric.connected = True
        self.connection = connection.StayAlive(self.pyric)
        self.connection.receive()
        assert self.pyric.connected == True

    def test_that_disconnect_event_happen_when_thread_completes(self):

        self.pyric.connected = False
        self.connection = connection.StayAlive(self.pyric)
        self.connection.run()

        call, e = self.pyric.events.pop()
        assert call == 'event'
        assert e.get('type') == 'disconnect'

        assert len(self.irc.events) == 0

    def test_that_receive_data_triggers_event(self):
        self.pyric.irc = self.irc
        self.connection = connection.StayAlive(self.pyric)

        self.irc.data = bytes(':vz!~vz@veiset.org PRIVMSG #brbot :hey!\n','UTF-8')
        self.connection.receive()

        call, e = self.pyric.events.pop()
        assert call == 'event'
        assert e.get('type') == 'PRIVMSG'
        assert len(self.irc.events) == 0
    
    def test_that_receive_data_will_not_parse_incomplete_data(self):
        self.connection = connection.StayAlive(self.pyric)

        self.irc.data = bytes(':vz!~vz@veiset.org PRIVMSG #brbot :hey!\n:vz!~vz@vei','UTF-8')
        self.connection.receive()
        assert self.connection.buffr == ':vz!~vz@vei'

        self.irc.data = bytes('set.org PRIVMSG #brbot :hey!\n','UTF-8')
        self.connection.receive()
        assert self.connection.buffr == ''

        
