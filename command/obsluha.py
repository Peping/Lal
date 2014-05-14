# -*- coding: utf-8 -*-
from threading import Timer
# https://docs.python.org/3.4/library/threading.html

from random import choice
# https://docs.python.org/3.4/library/random.html

def run(bot, nick, cmd, *args):
    bot.send(nick+": Vydrž chvilku, něco ti donesu!")
    Timer(2, step1, (bot,nick)).start()

def step1(bot, nick: str):
    bot.me("odkráčí odplíží k replikátoru syntetizovat něco dobrého.")
    Timer(20, step2, (bot,nick)).start()

def step2(bot, nick: str):
    # Vyber oslovení, to, co je před "Podává se X a k tomu Y jako příloha"
    osloveni = choice(("Voilà!", "Tady máš.", "Jsem zpátky.",
                       "Mmm, to to voní", "Dobrou chuť!",
                       "Bon apetit!", "Yatta!"))

    # Seznam možných jídel. Většítko (>) na začátku značí, že je jídlo
    # v množném čísle a má se použít "Podávají se" místo "Podává se"
    jidlo=["kuře", ">brambory", "citrón", "kyselina sirovodíková",
              "mateřské mléko", "šmirglpapír", "rýže", ">fazole",
              "máta", "vteřinové lepidýlko", ">střepy", "jar",
              ">kolíčky", "kytára", "krumpáč", "tvaroh", "hrášek",
              "pizza", "mrkev", "CD Evy a Vaška", "olej", "krupice",
              "párek", "Vysočina", "chléb Šumava", "cibule", "česnek",
              ">prdy jednorožců", ">smažené mnohonožky", "řízek",
              "cukr", "knedlik", ">halušky", ">bramboráky", "jablko",
              "židle", "pomsta", "pesík"]

    # Vyber jedno jídlo, a odeber ho ze seznamu. Pak vyber přílohu.
    # Tohle tu je, aby jedno jídlo nebyl hlavní chod a příloha zaráz
    jidlo1 = choice(jidlo)
    jidlo.remove(jidlo1)
    jidlo2 = choice(jidlo)

    # Kouzelný formátovací řetězec. Pokud znáte C#, určitě znáte i tohle
    bot.send("{4}: %C10{0}%C {3} %B{1}%B a k tomu %B{2}%B jako příloha.".format(
        osloveni, jidlo1.lstrip(">"), jidlo2.lstrip(">"),
        "Podává se" if jidlo1[0]!=">" else "Podávají se",
        nick
        )
    )