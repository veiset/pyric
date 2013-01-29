from pyric import *

class TestM():
    def __init__(self, bot):
        self.bot = bot
        self.bot.addListener("privmsg", self.test)

    def test(self, event):
        if event.get('message') == 'part':
            self.bot.part(info['channel'])

bot = Pyric("vzbottest", "vz", "vz", "irc.homelien.no", 6667)
testM = TestM(bot)
bot.connect()
bot.join('#brbot')
