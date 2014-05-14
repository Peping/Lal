# -*- coding: utf-8 -*-

from random import randint, choice
# https://docs.python.org/3.4/library/random.html

def run(bot, nick: str, cmd: str, *args):
    item=""
    with open("data/pumpac.txt") as f:
        item=choice(f.readlines())

    bot.send("{0}: %C10{1} %C%B{2}".format(
                 nick,
                 "Jsi" if randint(0,15)!=0 else "Vskutku nejsi",
                 item
                 )
            )