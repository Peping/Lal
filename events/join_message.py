# -*- coding: utf-8 -*-
import time
from datetime import datetime

def on_joined(bot,nick,**kw):
    if nick==bot.nickname:
        bot.send("%BAhoj, tak jsem se vrátila.%B Doufám, že jsem vám moc nechyběla.")
        return

    # Welcome message. First check if we know this nick
    last_seen=None
    with open("data/JoinsLeaves.csv","r") as f:
        f.seek(0,2)
        pos=f.tell()
        incomplete_line=""
        while pos>0:
            pos-=21
            f.seek(pos if pos>0 else 0)
            pos = f.tell()
            data = f.read(20)
            f.seek(pos)
            data = data.splitlines()
            lines = data[1:-1]
            incomplete_line=(data[-1]+incomplete_line) if len(data)>0 else ""
            if incomplete_line.count(" ")==2:
                lines+=[incomplete_line]

            lines = filter(lambda x: x[0]==nick , map(str.split,lines))
            line=None
            for line in lines: pass
            if line!=None:
                last_seen=float(line[2])
    if last_seen is not None:
        bot.send("%BVítej zpátky, {0}!%B Naposledy jsi tu byl {1}.".format(
                    nick, datetime.fromtimestamp(last_seen).strftime("%d. %m. %H:%M")
                    ))       
    else: 
        bot.send("%BAhoj, "+nick+"! Ještě jsem tě tu neviděla.%B Pokud potřebuješ pomoct, napiš !help")                

    with open("data/JoinsLeaves.csv","a") as f:
        f.write("{0} {1} {2}\n".format(nick,"joined",time.time()))


def on_left(bot,nick,**kw):
    with open("data/JoinsLeaves.csv","a") as f:
        f.write("{0} {1} {2}\n".format(nick,"left",time.time()))