import ircregex as regex
import re

class Event():
    def __init__(self, event, data={}):
        self.event = event
        self.data = data

    def add(self, key, value): self.data[key] = value
    def get(self, key): return self.data[key]
    def has(self, key): return key in self.data

def parse(data):
    ping = re.match(regex.PING, data)
    event = re.match(regex.EVENT, data)

    if ping: 
        e = Event('ping')
        e.add('pong', ping.group(1))
        return e

    elif event:
        prefix = event.group(1)
        command = event.group(2)
        param = event.group(3)

        if command == 'PART':
            params = param.split(':',1)
            channel = params[0]

            e = Event('part')
            e.add('user',    prefix)
            e.add('channel', channel)
            if len(params) > 1: e.add('message', param[1])

            return e

        elif command == 'JOIN':
            e = Event('join')
            e.add('user', prefix)
            e.add('channel', param)

            return e

        elif command == 'PRIVMSG':
            user, ident, host = re.split('[!@]', prefix)
            channel, message = param.split(':',1)

            e = Event('privmsg')
            e.add('user', user)
            e.add('ident', ident)
            e.add('host', host)
            e.add('channel', channel)
            e.add('private', not (channel[0] == '#'))
            e.add('message', message)

            return e

        else:
            e = Event(command.lower())
            e.add('param', param)
            
            return e

    else:
        return Event('unknown')

