#!/usr/bin/env python
__author__ = "python_guy"

from twisted.words.protocols import irc
from twisted.internet import protocol
import commands
import triggers
import thread



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

        # For some reason, the channel is always the sender's name,
        # instead of the receiver's name
        if channel == self.nickname:
            channel = nick

        # Now figure out if a command was given
        if msg.startswith("!"):
            # A command was given; parse it
            # If it has spaces, assume the command has arguments
            if msg.find(" ") != -1:
                command, args = msg[1:].split(" ", 1)
            # Otherwise, the command is just everything after the "!"
            else:
                command = msg[1:]
                args = ""

            # Check for the reload command (which relods the commands module)
            if command == "reload":
                reload(commands)
                reload(triggers)
                self.msg(channel, "Modules reloaded.")
            # Try to get the command from commands.py
            if hasattr(commands, command):
                # Run the command if it exists
                thread.start_new_thread(getattr(commands, command),(self, user, channel, args))


        # Check for silent triggers
        # (anything that doesn't require the bot to respond)
        # Load them from triggers.py so we can hot swap them
        triggers.process_message(self, user, channel, msg)


    def who(self, channel):
        "List the users in 'channel', usage: client.who('#testroom')"
        self.sendLine('WHO %s' % channel)

    def irc_RPL_WHOREPLY(self, *nargs):
        "Receive WHO reply from server"
        print 'WHO:', nargs

    def irc_RPL_ENDOFWHO(self, *nargs):
        "Called when WHO output is complete"
        print 'WHO COMPLETE'

    def irc_unknown(self, prefix, command, params):
        "Print all unhandled replies, for debugging."
        print 'UNKNOWN:', prefix, command, params






class PythonBotFactory(protocol.ClientFactory):
    protocol = PythonBot

    def __init__(self, channel, nickname="cobra_bot"):
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
    print "Connecting to database..."
    from pymongo import Connection
    connection = Connection()
    db = connection.rnyc_irc
    # TODO: Kinda lame
    commands.db = db
    triggers.db = db

    # Start the bot
    print "Connecting to IRC..."
    reactor.connectTCP("irc.freenode.net", 6667, PythonBotFactory(chan))
    reactor.run()
