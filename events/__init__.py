"""
Modul events

Tento modul se stará o vaše události. Události můžete definovat v jakémkoliv
souboru v adresáři events, ale nesmíte jeho jméno zapomenout přidat 
do proměnné __all__ v __init__.py

Handler události má tvar:

>>> def on_event(bot, **keyword_args)

Přičemž každá událost předává jiné argumenty. Seznam událostí a jejich
argumentů je v následující tabulce:

Event:             Parametry:       Popis:
"ctcp"             origin           Jméno odesilatele
                   is_request       Říká, jestli byl ctcp přijat jako NOTICE
                                    nebo jako PRIVMSG
                   command          CTCP příkaz jako řetězec
                   message          To, co následuje za příkazem
"query"            origin           Jméno odesilatele
                   message          Přijatá zpráva
"notice"           origin           Jméno odesilatele
                   message          Přijatá zpráva
"channel message"  origin           Jméno odesilatele
                   channel          Kanál ze kterého byla zpráva přijata
                   message          Přijatá zpráva
"channel notice"   origin           Jméno odesilatele
                   channel          Kanál ze kterého byla zpráva přijata
                   message          Přijatá zpráva
"joined"           nick             Přezdívka toho, co se připojil
                   channel          Kanál, na který se připojil
"left"             nick             Přezdívka toho, co se odpojil
                   channel          Kanál postižený odchodem
"nick"             nick             Původní přezdívka
                   new_nick         Nová přezdívka
"connected"        line             Celá neparsovaná zpráva z IRC serveru
"nick in use"      line             Celá neparsovaná zpráva z IRC serveru
"errorneous nick"  line             Celá neparsovaná zpráva z IRC serveru
"names"            line             Celá neparsovaná zpráva z IRC serveru
                   
Pozn: Bot automaticky "natvrdo" zpracovává následující události:
CTCP ping, PING od serveru, CTCP VERSION requesty, "connected", "nick in
use"

Na CTCP ping, PING a CTCP VERSION odpovídá podle IRC RFC specifikace.
V události connected se bot připojuje do místnosti a identifikuje 
přes NickServ.
Na nick in use bot reaguje přidáním podtržítka (_) za nick.                  

Event handler po napsání musíte zmínit ve funkci load souboru __init__.py
a to sice v sekci označené "Sem patří vaše event handlery". Za předpokladu,
že chcete reagovat na událost "channel message" a máte pro ni handler 
on_msg v souboru foo.py bude řádek, který přidáte do seznamu vypadat takto:

>>> HND("channel message",foo.on_msg)

Připomínám, že v tomto případě musí být "foo" v seznamu __all__ v souboru 
__init__.py

Debugging
---------

Silně doporučuji psát kód v něčem, co podporuje debugování. Já Lal psal
ve Visual studiu a vyplatilo se mi to. Bot všechny chyby zachytává, aby
při každé výjimce nespadnul. Stručný výpis chyby najdete v konzolovém okně.
"""

__all__=[
    "join_message",
    "not_a_robot"
    ]

from . import *
import traceback

handlers=[]

def load(bot):
    def HND(str, handler):
        def try_handler(**kw):
            try:
                handler(bot, **kw)
            except Exception as e: #Vypiš chybu, ale nepadej
                print("Error in handler for "+str+" ("+handler.__name__+"):")
                traceback.print_exc()

        return bot.add_handler(str,try_handler)

    ############################################
    #       Sem patří vaše event handlery      #
    ############################################

    handlers=[
        HND("joined",join_message.on_joined),
        HND("left",join_message.on_left),
        HND("channel message",not_a_robot.on_channel_msg),
    ]

def unload(bot):
    for handler in handlers:
        bot.remove_handler(handler)