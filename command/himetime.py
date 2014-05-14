# -*- coding: utf-8 -*-
import pytz
# http://pytz.sourceforge.net/

from datetime import datetime
# https://docs.python.org/3.4/library/datetime.html

def run(bot, nick: str, cmd: str, *args):
    mattovo_cas = datetime.now(pytz.timezone('Asia/Tokyo'))
    bot.send(u"Aktuální čas v Ósace je "+mattovo_cas.strftime(u"%X"))


