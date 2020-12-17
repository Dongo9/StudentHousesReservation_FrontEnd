import csv
import os
import sys
from pathlib import Path
from typing import Any, Tuple, Callable
import uuid
import hashlib

from py import std
from valid8 import validate, ValidationError

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
            .build()  # BUILDER PER LA COSTRUZIONE DEL MENU PRINCIPALE
        self.__database = Database()  # DICHIARO UN OGGETTO DATABASE
        try:
            self.__load_students()  # CARICO GLI STUDENTI
        except ValueError as e:
            print('--------------------------------------------')
            print('Continuing with an empty list of students...')
            print('--------------------------------------------')

        try:
            self.__load_admins()  # CARICO GLI ADMIN
        except ValueError as e:
            print('------------------------------------------')
            print('Continuing with an empty list of admins...')
            print('------------------------------------------')
        self.__logged_in_student = None  # OGGETTO PER TENERE TRACCIA DELL'UTENTE LOGGATO

    # ######################################### STUDENT ###############################################

    def __student_login(self) -> None:
        try:
            student = self.__read_student_credentials()  # LEGGE LE CREDENZIALI
            if self.__check_credentials(student):  # CHECK SULLE CREDENZIALI, SE VA BENE ALLORA ACCEDI AL MENU STUDENTE
                print('Successful login')
                print()
                self.__logged_in_student = student.matriculation_number
                self.__switch_to_students_menu()
            else:
                print('No account found with this credentials')  # ALTRIMENTI NON ACCEDE
                print()
        except (ValidationError, ValueError, TypeError):  # ECCEZIONE SE IL FORMATO E' ILLEGALE
            print('Access failed: please, choose to login and retry with correct credentials...')
            print()

    def __check_credentials(self, stud: Student) -> bool:
        for i in range(self.__database.students_size()):  # CHECK SULLA CORRISPONDENZA TRA I VARI STUDENTI
            st = self.__database.student(i)
            if st.__eq__(stud):
                return True
        return False

    def __read_student_credentials(self) -> Student:  # LETTURA CREDENZIALI STUDENT
        matriculation_number = self.__read('Matriculation Number', str)
        password = self.__read('Password', str)
        return Student(matriculation_number, password)

    def __add_reservation(self) -> None:  # AGGIUNTA RESERVATION

        if self.__database.has_already_reservation(self.__logged_in_student):  # SE HA GIA' LA RESERVATION,ALLORA CHIEDE
            print('Your new preferences will overwrite the previous ones, do you now? Y/N')
            val = input()
            try:
                validate('value', val, is_in=['Y', 'N'])
                if val == 'N':
                    print()
                    return
                elif val == 'Y':
                    print('I, lets go!')
                    print()
            except ValidationError:
                print('Invalid key entered, please choose to add a new reservation and retry with a correct one...')
                print()
                return

        try:
            reservation = self.__read_reservation() #LEGGE I DATI DELLA RESERVATION
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
            return #RESERVATION NON TROVATA

        res = self.__database.get_personal_reservation(self.__logged_in_student) #RETRIEVE DELLA RESERVATION

        print_sep = lambda: print('-' * 34)  # STAMPA DELLA RESERVATION
        print_sep()
        fmt = '%-20s %-20s'
        print(fmt % ('NEIGHBOURHOOD', 'ROOM_TYPE'))
        print_sep()

        print(fmt % (res.neighbourhood, res.room))

        print()
        print()

    def __logout(self) -> None: #EFFETTUA IL LOGOUT DELL''UTENTE
        self.__logged_in_student = None
        print('Successfully logged out from the system!')
        print()

    ########################################### ADMIN ####################################################

    def __admins_login(self) -> None: #EQUIVALENTE DI STUDENTE
        try:
            admin = self.__read_admin_credentials()
            if self.__check_admin_credentials(admin):
                print('Successful login')
                print()
                self.__switch_to_admins_menu()
            else:
                print('No account found with this credentials')
                print()
        except (ValidationError, ValueError, TypeError):
            print('Access failed: please, choose to login and retry with correct credentials...')
            print()

    def __read_admin_credentials(self) -> Admin: #EQUIVALENTE DI STUDENTE
        matriculation_number = self.__read('Matriculation Number', str)
        password = self.__read('Password', str)
        return Admin(matriculation_number, password)

    def __check_admin_credentials(self, admin: Admin) -> bool: #EQUIVALENTE DI STUDENTE
        for i in range(self.__database.admins_size()):
            ad = self.__database.admin(i)
            if ad.__eq__(admin):
                return True
        return False

    ########################################### MENU PRINCIPALE ################################################

    def __load_admins(self): #CARICO ADMIN
        if not Path(self.__adminsf).exists():
            return

        with open(self.__adminsf) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
            for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
                validate('row length', row, length=2)
                matriculation_number = row[0]
                password = row[1]
                self.__database.add_admin(Admin(matriculation_number, password))

    def __print_reservations(self) -> None: #STAMPO RESERVATIONS GENERALI
        print_sep = lambda: print('-' * 50)
        print_sep()
        fmt = '%-20s %-20s %-20s'
        print(fmt % ('NEIGHBOURHOOD', 'ROOM_TYPE', 'STUDENT'))
        print_sep()

        for key, value in self.__database.reservations().items():
            print(fmt % (value.neighbourhood, value.room, key))
        print()
        print()

    def __switch_to_admins_menu(self) -> None: #VIEW DEL MENU ADMIN
        self.__menu = Menu.Builder(Description('Administration panel'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Show all required reservations',
                                     on_selected=lambda: self.__print_reservations())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

        self.__menu.run()

    def __switch_to_students_menu(self) -> None: #VIEW DEL MENU STUDENTE
        self.__menu = Menu.Builder(Description('Students panel'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Add reservation', on_selected=lambda: self.__add_reservation())) \
            .with_entry(Entry.create('2', 'Retrieve your reservation',
                                     on_selected=lambda: self.__retrieve_your_reservation())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.__logout(), is_exit=True)) \
            .build()

        self.__menu.run()

    def __run(self) -> None: #RUN PER AVVIARE L'APPLICAZIONE
        try:
            self.__load()
        except ValueError as e:
            # print(e)
            print('------------------------------------------------')
            print('Continuing with an empty list of reservations...')
            print('------------------------------------------------')
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    def __load_students(self) -> None: #CARICA STUDENTI
        if not Path(self.__studentsf).exists():
            return

        with open(self.__studentsf) as file:
            reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
            for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
                validate('row length', row, length=2)
                matriculation_number = row[0]
                password = row[1]
                self.__database.add_student(Student(matriculation_number, password))

    def __load(self) -> None: #LOAD RESERVATIONS
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

    def __save(self) -> None: #SALVA LE RESERVATIONS SU FILE PRENDENDOLE DA RESERVATIONS DEL DB
        with open(self.__filename, 'w') as file:
            writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
            for key, value in self.__database.reservations().items():
                writer.writerow([value.neighbourhood, value.room, key])

    def hash_password(self, password): #UTILITY PER HASHARE LA PASSWORD CON SHA-256
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password): #CHECK SE LA PASSWORD CORRISPONDE A QUELLA NEL DB
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod #METODO STATICO PER LEGGERE L'INPUT E HASHARE LA PASSWORD
    def __read(prompt: str, builder: Callable) -> Any:
        if prompt == 'Password':
            while True:
                try:
                    line = hashlib.sha256(input(f'{prompt}: ').encode('utf-8')).hexdigest()
                    res = builder(line.strip())
                    return res
                except (TypeError, ValueError, ValidationError) as e:
                    print(e)
        else:
            while True:
                try:
                    line = line = input(f'{prompt}: ')
                    res = builder(line.strip())
                    return res
                except (TypeError, ValueError, ValidationError) as e:
                    print(e)

    def __read_reservation(self) -> Reservation: #LEGGE DA INPUT LA NUOVA RESERVATION
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
