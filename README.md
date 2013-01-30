pyric
=====

Event driven Python IRC library

Install
-------
```python setup.py install```

Example usage
-------------
```python
class PartModule():                                                                  
    ''' module for parting a channel '''                                         
    def __init__(self, bot):                                                     
        self.bot = bot                                                           
        self.bot.addListener("cmd.part", self.part)                               

    def part(self, event):                                                       
        if event.has('argv') and event.get('argv') == 'please':
            self.bot.part(event.get('channel'))
        else:
            self.bot.say(event.get('channel'), "Never!")

from pyric import *
bot = pyric.Pyric('vzbotte', 'vz', 'vz', 'irc.homelien.no', 6667)
bot.connect()
bot.join('#brbot')

m = PartModule(bot)
```

Running tests
-------------
Requires py.test

```py.test -v test/test_events.py```
