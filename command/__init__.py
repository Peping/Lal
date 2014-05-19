# -*- coding: utf-8 -*-
"""Modul s "veřejnými" příkazy.

Tento modul obsahuje všechny příkazy, co se dají spustit
napsáním !<příkaz> na kanál. Pokud napíšete nový příkaz, 
nezapomeňte jeho jméno dopsat do __all__ v souboru __init__.py

Soubor s příkazem musí obsahovat funkci run v následujícím tvaru:

>>> def run(bot, nick, cmd, *args):

Parametry:
bot : instance Lal
nick : přezdívka volajícího
cmd : název příkazu
*args : argumenty předané příkazu

Pokud například uživatel Franta napíše !kachna kvák kvák,
parametry předané funkci run v souboru kachna.py budou 
(bot, "Franta", "kachna", "kvák", "kvák"). Jestli si s pythonem
nejste dost jistí v kramflecích, větze, že *args spolkne ty
poslední 2 argumenty do n-tice (tuple). V args tedy bude
("kvák", "kvák").
"""

__all__=[
    "help",
    "himetime",
    "obsluha",
    "pumpac",
    "naposledy",
    ]

from . import *