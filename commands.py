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
        # user is in the format "nick_name!~real_name@host.name"
        uname = user.split("!", 1)[0]

    try:
        # Let the JSON module read in the response from Reddit's User API
        data = json.load(urllib2.urlopen("http://reddit.com/user/%s/about.json" % uname))["data"]
        # Feed the JSON-sourced dictionary to a format string
        self.msg(
            channel,
            "User: {name}  Link Karma: {link_karma}  Comment Karma: {comment_karma}".format(**data)
        )
    except urllib2.HTTPError, e:
        if e.code == 404:
            self.msg(channel, "User: %s does not exist." % uname)
        else:
            self.msg(channel, "Reddit is down!")
    except KeyError:
        # Happens when the data is malformed, and we can't get what we want from the JSON
        self.msg(channel, "Reddit broke :(")


def karma (self, user, channel, args):
    """ Responds with a list of karma records. """

    # Check for any sub-commands (like merge)
    args = args.split(" ")
    if args[0] == "merge":
        self.msg(channel, "Cut it out!")
        return
        old_karma = db.karma.find_one({"nick": args[1]})["karma"]
        new_karma = db.karma.find_one({"nick": args[2]})["karma"]
        new_karma += old_karma
        db.karma.update({"nick": args[2]}, {"$set": {"karma": new_karma}})
        db.karma.remove({"nick": args[1]})
        self.msg(channel, "%s + %s -> %s: %s" % \
                          (args[1], args[2], args[2], new_karma))
        return

    # TODO: Make this into a for loop if someone complains >_>
    # Put together a readable karma list, and display it'
    all = [x for x in db.karma.find()]
    all.sort(lambda x, y: cmp(y["karma"], x["karma"]))
    print all
    top_5 = all[:5]
    bottom_5 = all[-5:]
    karmaValues = lambda y: ", ".join(["%s(%s)" % (x["nick"], x["karma"]) for x in y])
    karma_text = "Top 5: %s | Bottom 5: %s" % (karmaValues(top_5), karmaValues(bottom_5))
    karma_text = karma_text.replace("<random>", str(random.randint(-1000, 1000)))
    
    self.msg(channel, str(karma_text))


def production (self, user, channel, args):
    if args == "join":
        self.join("#/r/nyc")
    elif args == "leave":
        self.leave("#/r/nyc")


def help (self, user, channel, args):
    """ Reponds with a list of commands. """

    commands = ["help", "karma", "rickroll"]
    commands.sort()
    self.msg(channel, "Commands: %s" % ", ".join(commands))


def reload_nick (self, user, channel, args):
    self.setNick("cobra_bot")


def src (self, user, channel, args):
    self.msg(channel, "https://github.com/uniite/rnyc_irc")
