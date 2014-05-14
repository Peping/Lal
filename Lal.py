#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Lal

Lal je robot pro IRC kanál irc.rizon.net/#vch . Je open source a je
psaný modulárně.
"""

import re
import time
import command
import events
import traceback
from IRC import IRC
from datetime import datetime
from importlib import reload as reload_module
from config import *

strip_accents_dict=dict( map(lambda x: (ord(x[0]),x[1]),
                    zip("äěščřžýáíéúůóňďťľôÄĚŠČŘŽÝÁÍÉÚŮÓŇĎŤĽÔ","aescrzyaieuuondtloAESCRZYAIEUUONDTLO")
                   ) )

def format_msg(msg):
    for pair in (("%%","¤×÷"),("%B","\x02"),("%C","\x03"),("%X","\x0F"),("¤×÷","%")):
        msg=msg.replace(*pair)

    return msg

class Lal(IRC):
    """Třída pro IRC bota Lal
    
Vlastnosti:
version - odpověď na ctcp version
nickname - nick bota
realname - realname bota
names - množina lidí na kanále (set)
    """
    def __init__(self):
        IRC.__init__(self,"irc.rizon.net")
        self.version = "Lal, robot pro #vch 0.0.1"
        self.nickname = NICKNAME
        self.realname = "Lal, VCh robot"
        self.names = set()

        self.add_handler("connected",lambda **kw: self.on_connect())
        self.add_handler("channel message",self.on_channel_message)
        self.add_handler("query",self.on_query)
        self.add_handler("nick in use", lambda **kw: self.nick(self.nickname+"_"))
        self.add_handler("names",self.on_names)
        self.add_handler("joined",lambda nick,**kw: self.names.add(nick))
        self.add_handler("left",lambda nick,**kw: self.names.discard(nick))
        self.add_handler("nick",lambda nick, new_nick,**kw: self.names.symmetric_difference_update(set((nick,new_nick))) if nick!=new_nick else None)


        events.load(self)

    def send(self, msg):
        """Odešle zprávu msg na kanál CHANNEL"""
        msg=format_msg(msg)
        IRC.msg(self,CHANNEL,msg)

    def msg(self, target, msg):
        """Odešle zprávu msg na kanál target nebo uživateli target"""
        msg=format_msg(msg)
        IRC.msg(self, target, msg)

    def notice(self, target, msg):
        """Odešle notice příjemci target"""
        msg=format_msg(msg)
        IRC.notice(self, target, msg)

    def me(self, msg, target=CHANNEL):
        """Odešle emote"""
        self.ctcp_command(target,"ACTION",(msg,))

    def on_connect(self):
        """Interní! Nevolat explicitně! Identifikuje bota pro NickServ a připojí se na CHANNEL"""
        if self.nickname!=NICKNAME:
            self.msg("NickServ", "GHOST Lal XXXXXXXXXX")
            self.nick(NICKNAME)

        self.msg("NickServ", "IDENTIFY Lal XXXXXXXXXX")
        self.join(CHANNEL)

    def on_names(self,line):
        self.names |= set((map(lambda x: x.strip("%+~@&"), line[line.find(":")+1:].split())))

    def on_channel_message(self,origin,message,**kw):
        """Zpracuje zprávu z kanálu, pokud obsahuje příkaz pro bota"""
        if message[0]=="!" and len(message)>1:
            split = message[1:].split()
            cmd = split[0].translate(strip_accents_dict)
            args = split[1:] if len(split)>1 else []
            self.bot_command(origin,cmd,*args)

    def on_query(self,origin,message,**kw):
        """Reaguje na !reload do query tak, že znovu načte eventy a příkazy. Nefunguje?"""
        if message=="!reload":
            try:
                reload_module(command)
            except SyntaxError:
                traceback.print_exc()
                self.msg(origin,"Syntax error v seznamu příkazů. Detaily v konzoli.")

            for module_name in filter(lambda x: not x.startswith('_'), dir(command)):
                try:
                    reload_module(getattr(command,module_name))
                except SyntaxError:
                    traceback.print_exc()
                    self.msg(origin,"Syntax error v příkazu "+module_name+". Detaily v konzoli.")


            events.unload(self)
            try:
                reload_module(events)
            except SyntaxError:
                traceback.print_exc()
                self.msg(origin,"Syntax error v seznamu eventů. Detaily v konzoli.")

            for module_name in filter(lambda x: not x.startswith('_'), dir(events)):
                try:
                    reload_module(getattr(events,module_name))
                except SyntaxError:
                    traceback.print_exc()
                    self.msg(origin,"Syntax error v eventu "+module_name+". Detaily v konzoli.")
                except BaseException:
                    pass
            events.load(self)

    def bot_command(self,origin, cmd, *args):
        """Zavolá korespondující příkaz pro bota z modulu command"""
        if cmd in filter(lambda x: not x.startswith('_'), dir(command)):
            try:
                getattr(command,cmd).run(self,origin,cmd,*args)
            except Exception as e:
                print("Error in !"+cmd+":")
                traceback.print_exc()

                self.notice(origin,"%C01,08× Příkaz %B!"+cmd+"%B selhal.%C10 Možná bys o tom měl dát vědět autorovi")
        else:
            self.notice(origin,"%C01,08× Příkaz %B!"+cmd+"%B neznám.%C10 Pro seznam příkazů napiš !help")

    

if __name__=="__main__":
    bot = Lal()
    bot.connect()