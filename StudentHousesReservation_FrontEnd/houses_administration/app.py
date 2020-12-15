import copy
import csv
import os
import sys
from pathlib import Path
from typing import Any, Tuple, Callable

from valid8 import validate, ValidationError

# TODO STAMPE DI ERRORE NON FUNZIONANO (CAUSA VALIDAZIONI)
from StudentHousesReservation_FrontEnd.houses_administration.domain import Database, Student, Reservation, Admin
from StudentHousesReservation_FrontEnd.houses_administration.menu import Menu, Entry, Description


class App:
    __filename = Path(__file__).parent.parent / 'reservations.csv'  # PERCORSO FILE RESERVATIONS
    __studentsf = Path(__file__).parent.parent / 'students.csv'  # PERCORSO FILE STUDENTI
    __adminsf = Path(__file__).parent.parent / 'admins.csv'  # PERCORSO FILE ADMINS
    __delimiter = '\t'

    def __init__(self):
        self.__menu = Menu.Builder(Description('Student houses reservations platform'),
                                   auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Login as student', on_selected=lambda: self.__student_login())) \
            .with_entry(Entry.create('2', 'Login as administrator', on_selected=lambda: self.__admins_login())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()
        self.__database = Database()
        self.__load_students()
        self.__load_admins()
        self.__logged_in_student = None

    ################################################################ STUDENT ####################################################################

    def __student_login(self) -> None:
        try:
            student = self.__read_student_credentials()
            if self.__check_credentials(student):
                print('Successful login')
                print()
                self.__logged_in_student = student.matriculation_number
                self.__switch_to_students_menu()
            else:
                print('No credentials found for this student')
                print()
        except (ValidationError, ValueError, TypeError): #AGGIUNGO QUI L'ECCEZIONE
            print('Access failed: please, choose to login and retry with correct credentials...')
            print()
            # os._exit(0)

    def __check_credentials(self, stud: Student) -> bool:
        for i in range(self.__database.students_size()):
            st = self.__database.student(i)
            if st.__eq__(stud):
                return True
        return False

    def __read_student_credentials(self) -> Student:
        matriculation_number = self.__read('Matriculation Number', str)
        password = self.__read('Password', str)
        return Student(matriculation_number, password)

    def __add_reservation(self) -> None:

        if self.__database.has_already_reservation(self.__logged_in_student):
            print('Your new preferences will overwrite the previous ones, do you now? Y/N')
            val = input()
            if val == 'N':
                return
            elif val == 'Y':
                print('I, lets go!')
                print()
        try:
            reservation = self.__read_reservation()
            self.__database.add_reservation(self.__logged_in_student, reservation)  # SCRITTURA SU "DB"
            self.__save()  # SCRITTURA SU FILE
            print('Reservation added')
        except ValidationError:
            print('Wrong values entered: please, choose to add a new reservation and retry with correct values...')
            print()

    def __retrieve_your_reservation(self) -> None:

        if self.__database.has_already_reservation(self.__logged_in_student) is False:
            print("No reservation found for your matriculation number")
            print()
            return

        res = self.__database.get_personal_reservation(self.__logged_in_student)

        print_sep = lambda: print('-' * 34)  # STAMPA POTREBBE ESSERE MESSA IN UN ALTRO METODO
        print_sep()
        fmt = '%-20s %-20s'
        print(fmt % ('NEIGHBOURHOOD', 'ROOM_TYPE'))
        print_sep()

        print(fmt % (res.neighbourhood, res.room))

        print()
        print()

    def __logout(self) -> None:
        self.__logged_in_student = None
        print('Successfully logged out from the system!')
        print()

    ########################################### ADMIN ####################################################

    def __admins_login(self) -> None:
        admin = Admin(*self.__read_admin_credentials())
        if self.__check_admin_credentials(admin):
            print('Successful access')
            self.__switch_to_admins_menu()
        else:
            print('Access failed, please retry with correct credentials...')

    def __read_admin_credentials(self) -> Tuple[str, str]:
        matriculation_number = self.__read('Matriculation Number', str)
        password = self.__read('Password', str)
        return matriculation_number, password

    def __check_admin_credentials(self, admin: Admin) -> bool:
        for i in range(self.__database.admins_size()):
            ad = self.__database.admin(i)
            if ad.__eq__(admin):
                return True
        return False

    ########################################### MENU PRINCIPALE ################################################

    def __load_admins(self):
        if not Path(self.__adminsf).exists():
            return

        with open(self.__adminsf) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
            for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
                validate('row length', row, length=2)
                matriculation_number = row[0]
                password = row[1]
                self.__database.add_admin(Admin(matriculation_number, password))

    def __print_reservations(self) -> None:
        print_sep = lambda: print('-' * 50)
        print_sep()
        fmt = '%-20s %-20s %-20s'
        print(fmt % ('NEIGHBOURHOOD', 'ROOM_TYPE', 'STUDENT'))
        print_sep()

        for key, value in self.__database.reservations().items():
            print(fmt % (value.neighbourhood, value.room, key))
        print()
        print()

    def __switch_to_admins_menu(self) -> None:
        self.__menu = Menu.Builder(Description('Administration panel'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Show all required reservations',
                                     on_selected=lambda: self.__print_reservations())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

        self.__menu.run()

    def __switch_to_students_menu(self) -> None:
        self.__menu = Menu.Builder(Description('Students panel'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Add reservation', on_selected=lambda: self.__add_reservation())) \
            .with_entry(Entry.create('2', 'Retrieve your reservation',
                                     on_selected=lambda: self.__retrieve_your_reservation())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.__logout(), is_exit=True)) \
            .build()

        self.__menu.run()

    def __run(self) -> None:
        try:
            self.__load()
        except ValueError as e:
            print(e)
            print('Continuing with an empty list of vehicles...')

        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __load_students(self) -> None:
        if not Path(self.__studentsf).exists():
            return

        with open(self.__studentsf) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
            for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
                validate('row length', row, length=2)
                matriculation_number = row[0]
                password = row[1]
                self.__database.add_student(Student(matriculation_number, password))

    def __load(self) -> None:
        if not Path(self.__filename).exists():  # SE IL PATH NON ESISTE, ALLORA NADA
            return

        with open(self.__filename) as file:  # APRE IL FLUSSO
            reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
            for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
                validate('row length', row, length=3)
                neighbourhood = row[0]
                room = row[1]
                student = row[2]
                self.__database.add_reservation(student, Reservation(neighbourhood, room))

    def __save(self) -> None:
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for key, value in self.__database.reservations().items():
                writer.writerow([value.neighbourhood, value.room, key])

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    def __read_reservation(self) -> Reservation:
        neighbourhood = self.__read('Neighbourhood (choose between these ones):\n'
                                        'NERVOSO\n'
                                        'MARTENSSONA\n'
                                        'MARTENSSONB\n'
                                        'MOLICELLEA\n'
                                        'MOLICELLEB\n'
                                        'MAISONETTES\n'
                                        'CHIODO1\n'
                                        'CHIODO2\n'
                                        'MONACI\n'
                                        'SANGENNARO\n', str)
        room_type = self.__read('Room (choose between SINGLE AND DOUBLE): ', str)
        return Reservation(neighbourhood, room_type)


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
