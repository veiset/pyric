pyric
=====

Event driven Python IRC library

Table of Contents
-----------------
* [1 - Installation](#1---installation)
* [2 - API documentation](#2---api-documentation)
* [3 - Usage](#3---example-usage)
* [3.1 - Simple example](#31---simple-example)
* [3.2 - Implementation example](#32---implementation-example)
* [Appendix - Testing](#appendix---testing)



1 - Installation
------------
This IRC framework uses Python 3. To install the bot type the following:

```bash
git clone http://github.com/veiset/pyric.git
cd pyric
python setup.py install
```

2 - API documentation
-----------------

3 - Example usage
-------------

3.1 - Simple example
--------------
In this simple example we will create an IRC bot that listens to the command ```.greet``` 
and replies with text ```Oh no you didn't!```. The bot will also ask people joining channle
```I like bacon, <username>. Do you?```.

```python
from pyric import *

bot = irc.Instance('simpleBot', 'vz', 'vz', 'irc.homelien.no', 6667)

def myHandler(event): 
    bot.irc.say(event.get("channel"), "Oh no you didn't!")
def myJoinHandler(event):
    bot.irc.say(event.get("channel"), "I like bacon, %s. Do you?" % event.get("nick"))
   
bot.addListener("cmd.greet", myHandler)
bot.addListiner("join", myJoinHandler)

bot.connect()
bot.join('#brbot')
```

Scenario:
```
       --> | simpleBot has joined #brbot
        vz | Welcom slave IRC bot!
        vz | .greet
 simpleBot | Oh no you didn't!
       --> | andern has joined #brbot
 simpleBot | I like bacon, andern. Do you?
```


3.2 - Implementation example
----------------------------
For an implementation example see the [Brunobot](http://github.com/veiset/Brunobot) IRC bot project.

Appendix - Testing
------------------
Requires py.test

```py.test -v test/test_events.py```
