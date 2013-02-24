import unittest
import mocks
import pyric.irc as irc 
import pyric.events as events

class LoggerTest(unittest.TestCase):
    
    def test_that_logger_prints_messages(self):
        log = irc.Logger()
        log.info('info')
        log.warn('warn')
        log.error('error')

        assert True

class IRCTest(unittest.TestCase):

    def setUp(self):

        irc.Logger = mocks.Log

        self.method1 = mocks.eventMethod1
        self.method2 = mocks.eventMethod2

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

    def test_adding_a_function_to_an_empty_event(self):
        self.pyric.addListener('join', self.method1)
        method = self.pyric.listeners['join'][0]

        assert len(self.pyric.listeners['join']) == 1
        assert method is self.method1 

    def test_that_adding_a_function_to_a_already_existing_event(self):
        self.pyric.addListener('join', self.method1)
        self.pyric.addListener('join', self.method2)

        method = self.pyric.listeners['join'][1]

        assert len(self.pyric.listeners['join']) == 2
        assert method is self.method2 

    def test_that_you_can_remove_a_function_from_an_event(self):
        self.pyric.addListener('join', self.method1)
        self.pyric.addListener('join', self.method2)

        assert len(self.pyric.listeners['join']) == 2
        self.pyric.removeListener('join', self.method2)
        assert len(self.pyric.listeners['join']) == 1

    def test_that_you_can_remove_a_function_from_an_event(self):

        self.pyric.addListener('join', self.method1)
        self.pyric.addListener('join', self.method2)

        assert len(self.pyric.listeners['join']) == 2
        self.pyric.removeListener('join', self.method2)
        assert len(self.pyric.listeners['join']) == 1

        method = self.pyric.listeners['join'][0]
        assert method is self.method1 

    def test_that_an_event_triggers_listening_functions(self):
        eventLogger = mocks.EventClass()
        self.pyric.addListener('join', eventLogger.method)
        self.pyric.addListener('join2', eventLogger.method)

        event = events.Event({'type' : 'join'})
        self.pyric.event(event)
        call, e = eventLogger.events.pop() 

        assert len(self.pyric.listeners['join']) == 1
        assert e == event
        assert len(eventLogger.events) == 0

    def test_that_an_event_triggers_listening_functions(self):
        event = events.Event({'type' : 'ping', 'msg' : 'data'})
        self.pyric.event(event)

        e, data = self.pyric.irc.events.pop()
        assert e == 'send'
        assert data == bytes('PONG data\r\n', 'UTF-8')
        assert len(self.pyric.irc.events) == 0
        
    def test_that_methods_listening_to_cmd_are_invoked_by_privmsg_cmds(self):
        eventLogger = mocks.EventClass()
        self.pyric.addListener('cmd.hello', eventLogger.method)

        event = events.Event({'type' : 'privmsg', 'msg' : '.hello data'})
        self.pyric.event(event)

        call, e = eventLogger.events.pop() 
        assert e == event
        assert len(eventLogger.events) == 0

    def test_disconnect_without_complications(self):
        self.pyric.connected = True
        self.pyric.disconnect()
       
        self.pyric.log.events.reverse()
        assert self.pyric.connected == False
        assert self.pyric.log.events.pop() == ('info','Bot terminated') 


    def test_disconnect_with_closed_socket(self):
        self.pyric.irc.send = mocks.throwMethod 

        self.pyric.connected = True
        self.pyric.disconnect()
        self.pyric.log.events.reverse()

        call, event = self.pyric.log.events.pop()
        assert call == 'warn'
        assert event == 'Could not communicate with IRC socket'

    def test_disconnect_with_closed_socket(self):
        self.pyric.irc.close = mocks.throwMethod 

        self.pyric.connected = True
        self.pyric.disconnect()
        self.pyric.log.events.reverse()

        call, event = self.pyric.log.events.pop()
        assert call == 'warn'
        assert event == 'Could not close the IRC socket. (Might already be closed)'

    def test_that_say_sends_message_to_socket(self):
        self.pyric.say('#brbot', 'hello')
        e, call = self.pyric.irc.events.pop()
        assert e == 'send'
        assert call == bytes('PRIVMSG #brbot :hello\r\n', 'UTF-8')
        assert len(self.pyric.irc.events) == 0

    def test_that_say_breaks_up_large_messages(self):
        msg = 'a'*700
        self.pyric.say('#brbot', msg)
        assert len(self.pyric.irc.events) == 2

