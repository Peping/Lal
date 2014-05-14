# -*- coding: utf-8 -*-
import command

def run(bot, nick: str, cmd: str, *args):
    cmds=filter(lambda x: not x.startswith('_') and x!="command", dir(command))
    bot.msg(nick, u"%BDostupné příkazy:%B "+" ".join(map(lambda x: "!"+x, cmds)) )