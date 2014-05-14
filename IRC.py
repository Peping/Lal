#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import socket
from re import match, search, sub
from uuid import uuid1 as uuid

class IRC:
    def __init__(self, server, port=6667, nick="", realname=""):
        self.server = server
        self.port = 6667
        self.nickname = nick
        self.realname = nick
        self.conn = None
        self.version = "IRC python generic custom bot 2014"

        self.events= {
                      "ctcp":{
                              uuid(): lambda is_request, origin, command, message: None if command.upper()!="PING" else self.ctcp_reply(origin,command,(message,)),
                              uuid(): lambda is_request, origin, command, message: None if command.upper()!="VERSION" else self.ctcp_reply(origin,command,(self.version,))
                             }
                      }

    def add_handler(self, event_name, handler):
        id= uuid()
        if event_name in self.events.keys():
            self.events[event_name][id] = handler
        else: self.events[event_name] = {id: handler}

        return id

    def remove_handler(self, event_name, handler_id):
        if event_name in self.events.keys():
            if handler_id in self.events[event_name].keys():
               del self.events[event_name]

    def clear_handlers(self, event_name):
        self.events[event_name] = {}

    def raise_event(self, event_name, **kwargs):
        if event_name not in self.events.keys():
            return

        for handler in self.events[event_name].values():
            handler(**kwargs)

    def connect(self):
        self.conn = socket.socket()
        file = self.conn.makefile(encoding="utf-8")
        self.conn.connect((socket.gethostbyname(self.server),
                                              self.port))

        self.nick(self.nickname)
        self.raw_command("USER",(self.nickname,self.nickname,self.nickname),self.realname)

        for line in file:
            if line[0]==":":
                line=line[1:].rstrip("\r\n")
                m = match("""([a-zA-Z0-9_\-\\\[\]{}\^`|]+)(!([^ ]*))? (.*)""",line)
                if m: self.parse_line (m.group(1), m.group(2), m.group(4))
                else: self.parse_other(line)      
            else:
                line = line.rstrip("\r\n")
                self.parse_other(line)


    def parse_line(self, nick, hostname, remainder):
        (argsstr, message) = remainder.split(" :",1) if " :" in remainder else (remainder.strip(),"")
        args = argsstr.split(" ")
        command = args[0]
        args = args[1:]

        if command=="PRIVMSG":
            if ord(message[0])==1 and ord(message[-1])==1:
                stripped = message[1:-1]
                first_space = stripped.find(" ")
                ctcp_command = stripped[:first_space] if first_space!=-1 else stripped
                ctcp_message = stripped[first_space+1:] if first_space!=-1 else ""
                self.raise_event("ctcp", is_request=True, origin=nick, message=ctcp_message, command=ctcp_command)
            elif len(args)==1:
                if args[0] == self.nickname:
                    self.raise_event("query",origin=nick, message=message)
                else: self.raise_event("channel message", origin=nick, channel=args[0], message=message)
        elif command=="NOTICE":
            if ord(message[0])==1 and ord(message[-1])==1:
                stripped = message[1:-1]
                first_space = stripped.find(" ")
                ctcp_command = stripped[:first_space] if first_space!=-1 else stripped
                ctcp_message = stripped[first_space+1:] if first_space!=-1 else ""
                self.raise_event("ctcp", is_request=False, origin=nick, message=ctcp_message, command=ctcp_command)
            elif len(args)==1:
                if args[0] == self.nickname:
                    self.raise_event("notice",origin=nick, message=message)
                else: self.raise_event("channel notice", origin=nick, channel=args[0], message=message)
        elif command=="JOIN":
            self.raise_event("joined", nick=nick, channel=message)
        elif command=="PART":
            self.raise_event("left", nick=nick, channel=message)
        elif command=="NICK":
            self.raise_event("nick", nick=nick, new_nick=message)

    def parse_other(self,line):
        ping_line = match("""PING :(.*)""", line)
        numbercode_line = match("""[^ ]* (\d{3}) """+self.nickname,line)
        if numbercode_line:
            numbercode = int(numbercode_line.group(1))
            self.raise_event({
                  1: "connected",
                433: "nick in use",
                432: "errorneous nick",
                353: "names"
            }.get( numbercode ),line = line)
        elif ping_line:
            self.raw_command("PONG",msg=ping_line.group(1))
        print(line)
                
    def ctcp_reply(self, target, command, args=()):
        self.raw_command("NOTICE",(target,),u'\x01'+command+" "+" ".join(args)+u'\x01')

    def ctcp_command(self, target, command, args=()):
        self.raw_command("PRIVMSG",(target,),u'\x01'+command+" "+" ".join(args)+u'\x01')

    def raw_command(self, command, args=(), msg=None):
        cmd = (command.upper()+
              ("" if len(args)==0 else " "+" ".join(args) )+
              ("" if msg is None else " :"+msg )+"\r\n").encode("utf-8")

        self.conn.sendall(cmd)

    def join(self, target):
        self.raw_command("JOIN",(target,))

    def msg(self, target, message):
        self.raw_command("PRIVMSG",(target,),message)

    def notice(self, target, message):
        self.raw_command("NOTICE",(target,),message)

    def nick(self, new_nick):
        self.nickname = new_nick
        self.raw_command("NICK",(new_nick,))