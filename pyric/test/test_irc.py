import unittest
import mocks
import pyric.irc as irc 

class ConnectionTest(unittest.TestCase):
    ''' Testing the connection '''

    def setUp(self):
        irc.Logger = mocks.Log

        self.ipaddr = '10.0.0.1'
        self.server = 'irc.veiset.org'
        self.port   = 6667
        self.nick   = 'vzbot'
        self.ident  = '~vz'
        self.name   = 'vz'

        self.pyric = irc.Instance(self.nick, 
                                  self.ident, 
                                  self.name, 
                                  self.server, 
                                  self.port,
                                  self.ipaddr)

        self.pyric.irc = mocks.Socket()


    def test_that_new_instance_contains_given_values(self):
        assert self.pyric.ipaddr == self.ipaddr 
        assert self.pyric.server == self.server 
        assert self.pyric.port   == self.port   
        assert self.pyric.nick   == self.nick   
        assert self.pyric.ident  == self.ident  
        assert self.pyric.name   == self.name   

    def test_that_socket_sends_data(self):
        self.pyric.connected = True
        self.pyric.send('Some random data...')
        e, data = self.pyric.irc.events.pop()

        assert e == 'send'
        assert len(self.pyric.irc.events) == 0

    def test_that_data_is_sent_as_bytes_with_carrige_return_linefeed(self):
        self.pyric.connected = True
        self.pyric.send('Data')
        e, data = self.pyric.irc.events.pop()

        assert e == 'send'
        assert data == bytes('Data'+ '\r\n','UTF-8')
        assert len(self.pyric.irc.events) == 0

    def test_that_join_sends_JOIN_to_irc_server(self):
        self.pyric.connected = True
        channel = '#brbot'
        self.pyric.join(channel)
        e, data = self.pyric.irc.events.pop()

        assert e == 'send'
        assert data == bytes('JOIN %s\r\n' % channel,'UTF-8')
        assert len(self.pyric.irc.events) == 0

    def test_that_part_sends_PART_to_irc_server(self):
        self.pyric.connected = True
        channel = '#brbot'
        self.pyric.part(channel)
        e, data = self.pyric.irc.events.pop()

        assert e == 'send'
        assert data == bytes('PART %s\r\n' % channel,'UTF-8')
        assert len(self.pyric.irc.events) == 0

    def test_that_mode_sends_MODE_to_irc_server(self):
        self.pyric.connected = True
        channel = '#brbot'
        mode    = '+o vz'
        self.pyric.mode(channel, mode)
        e, data = self.pyric.irc.events.pop()

        assert e == 'send'
        assert data == bytes('MODE %s %s\r\n' % (channel, mode),'UTF-8')
        assert len(self.pyric.irc.events) == 0

