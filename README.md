pyric
=====

Event driven Python IRC library

Install
-------
```python setup.py install```

Example usage
-------------
```python
from pyric import *
class Module():
    ''' module for parting a channel '''

    def __init__(self, bot):
        self.bot = bot
        self.bot.addListener("privmsg", self.test)

    def test(self, event):
        if event.get('message') == 'part':
            self.bot.part(info['channel'])

bot = Pyric("vzbottest", "vz", "vz", "irc.homelien.no", 6667)
module = Module(bot)
bot.connect()
bot.join('#brbot')
```
