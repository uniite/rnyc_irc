__author__ = "pyton_guy"

"""
Triggers for the #/r/nyc Freenode IRC bot

This module is used by bot.py and is separate so that it can be hot-swapped.
So if a trigger breaks, or a new one needs to be added, we don't need to
disconnect the bot from IRC to fix it. This bot is built for five-nines!
"""

import re


# Various regular expressions for finding commands in messages
# TODO: What characters are allowed in a nick?
# For finding karma
karma_regex = re.compile("([\w-]+)(\+\+|--)", re.M)


def process_message (self, user, channel, msg):
    # Karma Trigger
    for nick, points in karma_regex.findall(msg):
        # First, make sure the nick exists in the database
        if not db.karma.find_one({"nick": nick}):
            # Create it if it doesn't exist
            db.karma.insert({"nick": nick})
            # Mapping the "++" and "--" to numeric values
        # (I resisted the urge to make it a one-liner)
        if points == "++":
            points = +1
        else:
            points = -1
            # This will increment the nick's karma by the value of points
        db.karma.update({"nick": nick}, {"$inc": {"karma": points}})