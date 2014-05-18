# -*- coding: utf-8 -*-
import command
from config import *
from datetime import datetime

__author__ = 'Pohy'

def run(bot, nick: str, cmd: str, *args):
    try:
        target = args[0]
    except IndexError:
        bot.notice(nick,"Musíš mi říct jméno uživatele. (!naposledy uzivatel)")
        return

    if target==bot.nickname:
        bot.notice(nick,"Já tu jsem vždycky!")
        return

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

            lines = filter(lambda x: x[0]==target or (False if len(x)<=3 else x[2]==target) ,map(str.split, lines))
            line=None
            for line in lines: pass
            if line!=None:
                last_seen=float(line[2]) if len(line)<=3 else float(line[3])
    if last_seen is not None:
        bot.notice(nick,"%B{0}%B tu naposledy byl {1}.".format(
            target, datetime.fromtimestamp(last_seen).strftime("%d. %m. %H:%M")
        ))
    else:
        bot.notice(nick,target+" tu ještě nebyl.")

