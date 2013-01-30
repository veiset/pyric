import ircregex
import re

class Event():
    def __init__(self, event):
        self.event = event
        self.data = {}

    def add(self, key, value): self.data[key] = value
    def get(self, key): return self.data[key]
    def has(self, key): return key in self.data

def parse(data):
    ping = re.match(ircregex.PING, data)
    event = re.match(ircregex.EVENT, data)
    events = []

    if ping: 
        e = Event('ping')
        e.add('pong', ping.group(1))
        events.append(e)

    elif event:
        prefix = event.group(1)
        command = event.group(2)
        param = event.group(3)

        if command == 'PART':
            params = param.split(' :',1)
            channel = params[0]

            e = Event('part')
            e.add('user',    prefix)
            e.add('channel', channel)
            if len(params) > 1: e.add('message', params[1])

            events.append(e)

        elif command == 'JOIN':
            e = Event('join')
            e.add('user', prefix)
            e.add('channel', param[1:])

            events.append(e)

        elif command == 'PRIVMSG':
            user, ident, host = re.split('[!@]', prefix)
            channel, message = param.split(' :',1)

            e = Event('privmsg')
            e.add('user', user)
            e.add('ident', ident)
            e.add('host', host)
            e.add('channel', channel)
            e.add('private', not (channel[0] == '#'))
            e.add('message', message)

            events.append(e)

            if message.startswith('.') and len(message) > 1:
                cmd = message.split(' ',1)
                e = Event('cmd.' + cmd[0][1:])
                e.add('user', user)
                e.add('ident', ident)
                e.add('host', host)
                e.add('channel', channel)
                e.add('private', not (channel[0] == '#'))
                e.add('cmd', cmd[0])
                if len(cmd) > 1: e.add('argv', cmd[1])

                events.append(e)

        else:
            e = Event(command.lower())
            e.add('param', param)
            
            events.append(e)

    else:
       events.append(Event('unknown'))

    return events

