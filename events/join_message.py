# -*- coding: utf-8 -*-
import time
from datetime import datetime
from config import *

def on_joined(bot,nick,**kw):
    if nick==bot.nickname:
        bot.send("%BAhoj, tak jsem se vrátila.%B Doufám, že jsem vám moc nechyběla.")
        return

    # Welcome message. First check if we know this nick
    last_seen=None
    with open(JOINSLEAVES,"r") as f:
        f.seek(0,2)
        pos=f.tell()
        incomplete_line=""
        while pos>0:
            pos-=21
            f.seek(pos if pos>0 else 0)
            pos = f.tell()
            data = f.read()
            f.seek(pos)
            data = data.splitlines()
            lines = data[1:]

            lines = filter(lambda x: x[0]==nick or (False if len(x)<=3 else x[2]==nick) , map(str.split,lines))
            line=None
            for line in lines: pass
            if line!=None:
                last_seen=float(line[2]) if len(line)<=3 else float(line[3])
    if last_seen is not None:
        bot.send("%BVítej zpátky, {0}!%B Naposledy jsi tu byl {1}.".format(
                    nick, datetime.fromtimestamp(last_seen).strftime("%d. %m. %H:%M")
                    ))       
    else: 
        bot.send("%BAhoj, "+nick+"! Ještě jsem tě tu neviděla.%B Pokud potřebuješ pomoct, napiš !help")                

    with open(JOINSLEAVES,"a") as f:
        f.write("{0} {1} {2}\n".format(nick,"joined",time.time()))


def on_left(bot,nick,**kw):
    with open(JOINSLEAVES,"a") as f:
        f.write("{0} {1} {2}\n".format(nick,"left",time.time()))

def on_nick(bot,nick,new_nick,**kw):
    with open(JOINSLEAVES,"a") as f:
        f.write("{0} renamed {1} {2}\n".format(nick, new_nick, time.time()))