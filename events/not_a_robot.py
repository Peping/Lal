# -*- coding: utf-8 -*-
import re

def on_channel_msg(bot,origin,message,**kw):
    if re.search(r"\b(ro)?bot",message,re.IGNORECASE) and bot.nickname in message:
            bot.send(origin+": Já nejsem robot, jsem android.")