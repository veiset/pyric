import pytest
from pyric import events

server          = 'irc.server.com'
nick            = 'vz'
ident           = '~vz'
host            = 'veiset.org'
user            = '%s!%s@%s' % (nick, ident, host)
chan            = '#brbot'
msg             = 'hello, and goodbye'

event_PING      = 'PING :%s'             # (server)
event_PART_MSG  = ':%s PART %s :%s'      # (user, chan, msg)
event_PART      = ':%s PART %s'          # (user, chan)
event_JOIN      = ':%s JOIN :%s'         # (user, chan)
event_PRIVMSG   = ':%s PRIVMSG %s :%s'   # (user, chan, msg)
event_CMD       = ':%s PRIVMSG %s :.cmd' # (user, chan)


# Event Types 
def test_parsePingReturnsOnePingEvent():
    event = events.parse(event_PING % server)
    assert event[0].event == 'ping'

def test_parseJoinReturnsOneJoinEvent():
    event = events.parse(event_JOIN % (user, chan))
    assert event[0].event == 'join'

def test_parsePartReturnsOnePartEvent():
    event = events.parse(event_PART % (user, chan))
    assert event[0].event == 'part'

def test_parsePartWMsgReturnsOnePartEvent():
    event = events.parse(event_PART_MSG % (user, chan, msg))
    assert event[0].event == 'part'

def test_parsePrivmsgReturnsOnePrivmsg():
    event = events.parse(event_PRIVMSG % (user, chan, msg))
    assert event[0].event == 'privmsg'

def test_parseCmdIsBothPrivmsgEventAndCmdEvent():
    privmsg, cmd = events.parse(event_CMD % (user, chan))
    assert privmsg.event == 'privmsg'
    assert cmd.event.startswith('cmd.')

def test_parseCmdWithArgvContainsArgv():
    cmd = events.parse(event_CMD % (user, chan) + ' arg1 arg2')[1]
    assert cmd.event.startswith('cmd.')
    assert cmd.get('argv') == 'arg1 arg2'

# Event Types has correct data
def test_pingEventContainsParsedData():
    ping = events.parse(event_PING % server)[0]
    assert ping.get('pong') == server

def test_joinEventContainsParsedData():
    join = events.parse(event_JOIN % (user, chan))[0]
    assert join.get('user') == user
    assert join.get('channel') == chan

