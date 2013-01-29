import ircregex as regex
import re

def parse(data):
    ping = re.match(regex.PING, data)
    event = re.match(regex.EVENT, data)

    if ping: 
        return ('ping', {'pong' : ping.group(1)})
    elif event:
        prefix = event.group(1)
        command = event.group(2)
        param = event.group(3)


        if command == 'PART':
            params = param.split(':',1)
            channel = params[0]
            if len(params) > 1: message = params[1]
            else: message = ''
            info = {'user'    : prefix,
                    'channel' : channel,
                    'message' : message}
            return ('part', info)
        elif command == 'JOIN':
            info = {'user'    : prefix,
                    'channel' : param}
            return ('join', info)
        elif command == 'PRIVMSG':
            user, ident, host = re.split('[!@]', prefix)
            channel, message = param.split(':',1)
            info = {'user'    : user,
                    'ident'   : ident,
                    'host'    : host,
                    'channel' : channel,
                    'private' : not (channel[0] == '#'),
                    'message' : message}
            return ('privmsg', info)
        else:
            return (command.lower(), 
                    {'command' : command,
                     'param'   : param})
    else:
        return ('unknown', {'data' : data}) 

