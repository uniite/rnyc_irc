__author__ = "pyton_guy"

"""
Commands for the #/r/nyc Freenode IRC bot

This module is used by bot.py and is separate so that it can be hot-swapped.
So if a command breaks, or a new one needs to be added, we don't need to
disconnect the bot from IRC to fix it. This bot is built for five-nines!
"""


def karma (self, user, channel, args):
    """ Responds with a list of karma records. """

    # TODO: Make this into a for loop if someone complains >_>
    # Put together a readable karma list, and display it'
    karma_text = ", ".join([
                           "%s: %s" % (record["nick"], record["karma"])
                           for record in db.karma.find()
                           ])
    self.msg(channel, str(karma_text))


def help (self, user, channel, args):
    """ Reponds with a list of commands. """

    commands = ["help", "karma", "this wasn't here before"]
    commands.sort()
    self.msg(channel, "Commands: %s" % ", ".join(commands))

