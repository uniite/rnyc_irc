__author__ = "pyton_guy"

"""
Commands for the #/r/nyc Freenode IRC bot

This module is used by bot.py and is separate so that it can be hot-swapped.
So if a command breaks, or a new one needs to be added, we don't need to
disconnect the bot from IRC to fix it. This bot is built for five-nines!
"""

import random
import urllib2
import json

def reddit(self, user, channel, args):
    if args:
        uname = args
    else:
        uname = user

    try:
        response = urllib2.urlopen('http://reddit.com/user/%s/about.json' % uname)
    except urllib2.HttpError:
        self.msg(channnel, "User: %s does not exist." % uname)
        return

    jsn = response.read()
    
    data = json.loads(jsn)
    lk=data['link_karma']
    ck=data['comment_karma']
    
    self.msg(channel, "User: "+uname+" Link Karma: "+lk+" Comment Karma: "+ck)

def karma (self, user, channel, args):
    """ Responds with a list of karma records. """

    # TODO: Make this into a for loop if someone complains >_>
    # Put together a readable karma list, and display it'
    karma_text = ", ".join([
                           "%s: %s" % (record["nick"], record["karma"])
                           for record in db.karma.find()
                           ])
    karma_text = karma_text.replace("<random>", str(random.randint(1, 1000)))
    
    self.msg(channel, str(karma_text))


def production (self, user, channel, args):
    if args == "join":
        self.join("#/r/nyc")
    elif args == "leave":
        self.leave("#/r/nyc")


def help (self, user, channel, args):
    """ Reponds with a list of commands. """

    commands = ["help", "karma", "this wasn't here before"]
    commands.sort()
    self.msg(channel, "Commands: %s" % ", ".join(commands))

