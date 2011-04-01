#!/usr/bin/env python
__author__ = "python_guy"

from twisted.words.protocols import irc
from twisted.internet import protocol
import re
import commands




# Various regular expressions for finding commands in messages
# TODO: What characters are allowed in a nick?
# For finding karma
karma_regex = re.compile("([\w-]+)([\+-]{2})", re.M)

class PythonBot(irc.IRCClient):
    """ An IRC bot for #/r/nyc on freenode. """

    
    def _get_nickname(self):
        """ Gets this bot's nickname. """
        return self.factory.nickname
    
    # A property to get this bot's nickname
    nickname = property(_get_nickname)


    def signedOn (self):
        """ Joins the channel once the bot is signed onto the IRC server. """

        self.join(self.factory.channel)
        print "Signed on as %s." % (self.nickname,)


    def privmsg(self, user, channel, msg):
        """
        Called whenever a message is sent to us or to a channel we're in.
        """

        # Ignore bad messages
        if not user:
            return
        # Try to figure out the nick of the user messaging us
        # They come int he format "python_guy!~python_gu@www2.comefind.me"
        nick = user.split("!", 1)[0]

        # Now figure out if a command was given
        if msg.startswith("!"):
            # A command was given; parse it
            # If it has spaces, assume the command has arguments
            if msg.find(" ") != -1:
                command , args = msg[1:].split(" ", 1)
            # Otherwise, the command is just everything after the "!"
            else:
                command = msg[1:]
                args = ""

            # Check for the reload command (which relods the commands module)
            if command == "reload":
                reload(commands)
                self.msg(channel, "Commands reloaded.")
            # Try to get the command from commands.py
            if hasattr(commands, command):
                # Run the command if it exists
                getattr(commands, command)(self, user, channel, args)


        # Check for silent triggers
        # (anything that doesn't require the bot to respond)
        
        # Karma Trigger
        for nick, points in karma_regex.findall(msg):
            # First, make sure the nick exists in the database
            if not db.karma.find_one({"nick": nick}):
                # Create it if it doesn't exist
                db.karma.insert({"nick": nick, "value": 0})
            # Mapping the "++" and "--" to numeric values
            # (I resisted the urge to make it a one-liner)
            if points == "++":
                points = +1
            else:
                points = -1
            # This will increment the nick's karma by the value of points
            db.karma.update({"nick": nick}, {"$inc": {"karma": points}})





class PythonBotFactory(protocol.ClientFactory):
    protocol = PythonBot

    def __init__(self, channel, nickname="python_bot"):
        self.channel = channel
        self.nickname = nickname

    def clientConnectionLost(self, connector, reason):
        print "Lost connection (%s), reconnecting." % (reason,)
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print "Could not connect: %s" % (reason,)


import sys
from twisted.internet import reactor

if __name__ == "__main__":
    # Figure out what channel to go on
    if len(sys.argv) > 1:
        chan = sys.argv[1]
    else:
        chan = "#/r/nyc-test"

    # Connect to the DB
    from pymongo import Connection
    connection = Connection()
    db = connection.rnyc_irc
    # TODO: Kinda lame
    commands.db = db

    # Start the bot
    reactor.connectTCP("irc.freenode.net", 6667, PythonBotFactory(chan))
    reactor.run()
