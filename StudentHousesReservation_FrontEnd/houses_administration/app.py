import csv
import sys
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

from StudentHousesReservation_FrontEnd.houses_administration.domain import *
from StudentHousesReservation_FrontEnd.houses_administration.menu import Menu, Entry, Description


class App:
    __filename = Path(__file__).parent.parent / 'default.csv'
    __delimiter = '\t'
    __status: str = 0
    __menu: Menu

    def __init__(self):
        self.switcher(0)

    def printciao(self):
        print("paolobello")

    def __run(self) -> None:
        # try:
        #    self.__load()
        # except ValueError as e:
        #   print(e)
        #   print('Continuing with an empty list of vehicles...')
        self.__menu.switcher(0)

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def menu0(self):
        return Menu.Builder(Description('Welcome to Student House Reservation for Unical. \n '
                                        '            )                     \n'
                                        '           (      _[]_         (  \n'
                                        '   __[]___[]___[]/____\_[]_    )  \n'
                                        '  /______________|[][]|____\  (   \n'
                                        '  |[][]|[][]|[][]|[][]|[][]|__[]_ \n'
                                        '  |  /\|/\  |  /\|  /\|/\  |_____|\n'
                                        '  |[]|||||[]|[]|||[]|||||[]|[_]|||\n'
                                        'Who do you want to access as ?')) \
            .with_entry(Entry.create('1', 'Student', on_selected=lambda: self.switcher(1))) \
            .with_entry(Entry.create('2', 'Staff', on_selected=lambda: self.switcher(1))) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

    def menu1(self):
        return Menu.Builder(Description('Welcome to Student House Reservation for Unical. \n '
                                        'Who do you want to access as ?')) \
            .with_entry(Entry.create('1', 'Student', on_selected=lambda: self.switcher(0))) \
            .with_entry(Entry.create('2', 'Staff', on_selected=lambda: self.printciao(), is_exit=True)) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

    def switcher(self, stat: int):

        self.__status = stat
        if self.__status == 0:
            self.__menu = self.menu0()

        elif self.__status == 1:
            self.__menu = self.menu1()

        # set_menu = globals()["menu" + self.status]
        # self.menu = set_menu()

        self.__menu.run()

    def __set_status(self, stat: int):
        self.__status = stat


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
