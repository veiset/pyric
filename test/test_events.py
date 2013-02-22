import pytest
from pyric import events

server          = 'irc.server.com'
nick            = 'vz'
ident           = '~vz'
host            = 'veiset.org'
user            = '%s!%s@%s' % (nick, ident, host)
chan            = '#brbot'
msg             = 'hello, and goodbye'
users           = '@vz Ymgve Snuskotin +brunobto andern mn'

event_PING      = 'PING :%s'             # (server)
event_PART_MSG  = ':%s PART %s :%s'      # (user, chan, msg)
event_PART      = ':%s PART %s'          # (user, chan)
event_JOIN      = ':%s JOIN :%s'         # (user, chan)
event_PRIVMSG   = ':%s PRIVMSG %s :%s'   # (user, chan, msg)
event_CMD       = ':%s PRIVMSG %s :.cmd' # (user, chan)
event_353       = ':%s 353 %s = %s :%s' # (server, user, chan, users)

# Event Types 
def test_parse353NamesEvent():
    event = events.parse(event_353 % (server, user, chan, users))
    assert event[0].event == 'names'

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


# Event Types parse the data correctly
def test_namesEventContainsParsedData():
    names = events.parse(event_353 % (server, user, chan, users))[0]
    assert names.get('users') == users.split(' ')

def test_pingEventContainsParsedData():
    ping = events.parse(event_PING % server)[0]
    assert ping.get('pong') == server

def test_joinEventContainsParsedData():
    join = events.parse(event_JOIN % (user, chan))[0]
    assert join.get('user') == user
    assert join.get('channel') == chan

def test_partEventContainsParsedData():
    part = events.parse(event_PART % (user, chan))[0]
    assert part.get('user') == user
    assert part.get('channel') == chan 
    assert not part.has('message')

def test_partEventWMsgContainsParsedData():
    part = events.parse(event_PART_MSG % (user, chan, msg))[0]
    assert part.get('user') == user
    assert part.get('channel') == chan 
    assert part.get('message') == msg

def test_privmsgEventContainsParsedData():
    user = '%s!%s@%s' % (nick, ident, host)
    privmsg = events.parse(event_PRIVMSG % (user, chan, msg))[0]
    assert privmsg.get('user') == nick 
    assert privmsg.get('ident') == ident
    assert privmsg.get('host') == host
    assert privmsg.get('channel') == chan
    assert privmsg.get('private') == False
    assert privmsg.get('message') == msg

def test_privatePrivmsgEventContainsParsedData():
    user = '%s!%s@%s' % (nick, ident, host)
    chan = 'nickname'
    privmsg = events.parse(event_PRIVMSG % (user, chan, msg))[0]
    assert privmsg.get('user') == nick 
    assert privmsg.get('ident') == ident
    assert privmsg.get('host') == host
    assert privmsg.get('channel') == chan
    assert privmsg.get('private') == True 
    assert privmsg.get('message') == msg

def test_cmdNoArgvEventContainsParsedData():
    user = '%s!%s@%s' % (nick, ident, host)
    msg = '.cmd'
    cmd = events.parse(event_PRIVMSG % (user, chan, msg))[1]
    assert cmd.get('user') == nick 
    assert cmd.get('ident') == ident
    assert cmd.get('host') == host
    assert cmd.get('channel') == chan
    assert cmd.get('private') == False 
    assert cmd.get('cmd') == msg

def test_cmdNoArgvEventContainsParsedData():
    user = '%s!%s@%s' % (nick, ident, host)
    command = '.cmd'
    argv = 'arg1 arg2'
    cmd = events.parse(event_PRIVMSG % (user, chan, command + ' ' + argv))[1]
    assert cmd.get('user') == nick 
    assert cmd.get('ident') == ident
    assert cmd.get('host') == host
    assert cmd.get('channel') == chan
    assert cmd.get('private') == False 
    assert cmd.get('cmd') == command
    assert cmd.get('argv') == argv
