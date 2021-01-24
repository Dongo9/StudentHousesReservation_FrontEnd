import csv
import requests
import sys
from pathlib import Path
from typing import Any, Tuple, Callable
import uuid
import hashlib

from py import std
from valid8 import validate, ValidationError

from StudentHousesReservation_FrontEnd.houses_administration.domain import Database, Student, Reservation, Employee, \
    Neighbourhood
from StudentHousesReservation_FrontEnd.houses_administration.menu import Menu, Entry, Description

api_server = 'http://localhost:8000/api/v1/'


class App:
    # __filename = Path(__file__).parent.parent / 'reservations.csv'  # PERCORSO FILE RESERVATIONS
    # __studentsf = Path(__file__).parent.parent / 'students.csv'  # PERCORSO FILE STUDENTI
    # __adminsf = Path(__file__).parent.parent / 'admins.csv'  # PERCORSO FILE ADMINS
    # __delimiter = '\t'
    __key = None

    def __init__(self):
        self.__menu = Menu.Builder(Description('Student houses reservations platform'),
                                   auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Login as student', on_selected=lambda: self.__student_login())) \
            .with_entry(Entry.create('2', 'Login as employee', on_selected=lambda: self.__employee_login())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()  # BUILDER PER LA COSTRUZIONE DEL MENU PRINCIPALE
        # self.__database = Database()  # DICHIARO UN OGGETTO DATABASE
        self.__logged_in_student = None  # OGGETTO PER TENERE TRACCIA DELL'UTENTE LOGGATO (salvo solo matricola)

    # ######################################### STUDENT ###############################################

    def __student_login(self) -> None:
        try:
            student = self.__read_student_credentials()  # LEGGE LE CREDENZIALI

            res = requests.post(url=f'{api_server}auth/login/',
                                data={'username': student.matriculation_number, 'password': student.password})

            if res.status_code == 200:
                print('SUCCESSFUL LOGIN')
                print()
                self.__logged_in_student = student
                self.__key = res.json()['key']
                #print(self.__key)
                self.__switch_to_students_menu()
            else:
                print('No account found with these credentials')
                print()

        except (ValidationError, ValueError, TypeError):  # ECCEZIONE SE IL FORMATO E' ILLEGALE
            print('Access failed: please, choose to login and retry with correctly typed credentials...')
            print()

    def __read_student_credentials(self) -> Student:  # LETTURA CREDENZIALI STUDENT
        matriculation_number = input('Matriculation Number: ')
        password = input('Password: ')
        return Student(matriculation_number, password)

    def __add_reservation(self) -> None:  # AGGIUNTA RESERVATION
        try:
            res = requests.get(url=f'{api_server}reservation-student/',
                               headers={'Authorization': f'Token {self.__key}'})

            if res.status_code == 200:

                reservation = self.__read_reservation()

                if len(res.json()) == 0:
                    res = requests.post(url=f'{api_server}reservation-student/add/',
                                        headers={'Authorization': f'Token {self.__key}'},
                                        data={'neighborhood': reservation.neighbourhood, 'room_type': reservation.room})

                    if res.status_code == 201:
                        print("Reservation successfully added")

                    else:
                        print("Something went wrong with reservation adding")

                else:

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
                        print(
                            'Invalid key entered, please choose to add a new reservation and retry with a correct one...')
                        print()
                        return

                    reservation_id = res.json()[0]['id']

                    res_edit = requests.patch(url=f'{api_server}reservation-student/edit/{reservation_id}/',
                                              headers={'Authorization': f'Token {self.__key}'},
                                              data={'neighborhood': reservation.neighbourhood,
                                                    'room_type': reservation.room})

                    if res_edit.status_code == 200:
                        print('Reservation successfully updated')
                    else:
                        print('Something went wrong with reservation updating...')
            return
        except ValidationError:
            print('Invalid key entered, please choose to add a new reservation and retry with a correct one...')
            print()
            return

    def __retrieve_your_reservation(self) -> None:

        res = requests.get(url=f'{api_server}reservation-student/', headers={'Authorization': f'Token {self.__key}'})

        if res.status_code == 200:
            if len(res.json()) == 0:
                print('No reservation found for your matriculation number')

            else:
                print_sep = lambda: print('-' * 34)  # STAMPA DELLA RESERVATION
                print_sep()
                fmt = '%-20s %-20s'
                print(fmt % ('NEIGHBOURHOOD', 'ROOM_TYPE'))
                print_sep()

                print(fmt % (res.json()[0]['neighborhood'], res.json()[0]['room_type']))

        else:
            print("Something went wrong with your request: RIPIT")
            print()
            return

    def __logout(self) -> None:  # EFFETTUA IL LOGOUT DELL''UTENTE
        self.__logged_in_student = None
        print('Successfully logged out from the system!')
        print()

    ########################################### ADMIN ####################################################

    def __employee_login(self) -> None:  # EQUIVALENTE DI STUDENTE
        try:
            employee = self.__read_admin_credentials()

            res = requests.post(url=f'{api_server}auth/login/',
                                data={'username': employee.username, 'password': employee.password})

            if res.status_code == 200:
                print('SUCCESSFUL LOGIN')
                print()
                self.__key = res.json()['key']
                print(self.__key)
                self.__switch_to_admins_menu()

            else:
                print('No account found with these credentials')
                print()
        except (ValidationError, ValueError, TypeError):
            print('Access failed: please, choose to login and retry with correct credentials...')
            print()

    def __read_admin_credentials(self) -> Employee:  # EQUIVALENTE DI STUDENTE
        username = input('Username: ')
        password = input('Password: ')
        return Employee(username, password)

    ########################################### MENU PRINCIPALE ################################################

    # def __load_admins(self):  # CARICO ADMIN
    #    if not Path(self.__adminsf).exists():
    #        return
    #
    #    with open(self.__adminsf) as file:
    #        reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
    #        for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
    #            validate('row length', row, length=2)
    #            matriculation_number = row[0]
    #            password = row[1]
    #            self.__database.add_admin(Employee(matriculation_number, password))

    def __print_reservations(self) -> None:  # STAMPO RESERVATIONS GENERALI

        res = requests.get(url=f'{api_server}reservation-list/', headers={'Authorization': f'Token {self.__key}'})

        print_sep = lambda: print('-' * 50)
        print_sep()
        fmt = '%-20s %-20s %-20s'
        print(fmt % ('NEIGHBOURHOOD', 'ROOM_TYPE', 'STUDENT'))
        print_sep()

        for item in res.json():
            print(fmt % (item['neighborhood'], item['room_type'], item['user']))
        print()
        print()

    def __switch_to_admins_menu(self) -> None:  # VIEW DEL MENU ADMIN
        self.__menu = Menu.Builder(Description('Administration panel'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Show all required reservations',
                                     on_selected=lambda: self.__print_reservations())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print('Bye!'), is_exit=True)) \
            .build()

        self.__menu.run()

    def __switch_to_students_menu(self) -> None:  # VIEW DEL MENU STUDENTE

        self.__menu = Menu.Builder(Description('Students panel'), auto_select=lambda: None) \
            .with_entry(Entry.create('1', 'Add reservation', on_selected=lambda: self.__add_reservation())) \
            .with_entry(Entry.create('2', 'Retrieve your reservation',
                                     on_selected=lambda: self.__retrieve_your_reservation())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.__logout(), is_exit=True)) \
            .build()

        self.__menu.run()

    def __run(self) -> None:  # RUN PER AVVIARE L'APPLICAZIONE
        self.__menu.run()

    def run(self) -> None:
        try:
            self.__run()
        except:
            print('Panic error!', file=sys.stderr)

    # def __load_students(self) -> None:  # CARICA STUDENTI
    #    if not Path(self.__studentsf).exists():
    #        return
    #
    #    with open(self.__studentsf) as file:
    #        reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
    #        for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
    #            validate('row length', row, length=2)
    #            matriculation_number = row[0]
    #            password = row[1]
    #            self.__database.add_student(Student(matriculation_number, password))

    # def __load(self) -> None:  # LOAD RESERVATIONS
    #    if not Path(self.__filename).exists():  # SE IL PATH NON ESISTE, ALLORA NADA
    #        return
    #
    #    with open(self.__filename) as file:  # APRE IL FLUSSO
    #        reader = csv.reader(file, delimiter=self.__delimiter)  # DICHIARA LETTORE FILE .CSV
    #        for row in reader:  # PER OGNI RIGA, INDIVIDUA LA TUPLA DA MEMORIZZARE
    #            validate('row length', row, length=3)
    #            neighbourhood = row[0]
    #            room = row[1]
    #            student = row[2]
    #            self.__database.add_reservation(student, Reservation(neighbourhood, room))

    # def __save(self) -> None:  # SALVA LE RESERVATIONS SU FILE PRENDENDOLE DA RESERVATIONS DEL DB
    #    with open(self.__filename, 'w') as file:
    #        writer = csv.writer(file, delimiter=self.__delimiter, lineterminator='\n')
    #        for key, value in self.__database.reservations().items():
    #            writer.writerow([value.neighbourhood, value.room, key])

    def hash_password(self, password):  # UTILITY PER HASHARE LA PASSWORD CON SHA-256
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    def check_password(self, hashed_password, user_password):  # CHECK SE LA PASSWORD CORRISPONDE A QUELLA NEL DB
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @staticmethod  # METODO STATICO PER LEGGERE L'INPUT E HASHARE LA PASSWORD
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

    def __read_reservation(self) -> Reservation:  # LEGGE DA INPUT LA NUOVA RESERVATION
        neighbourhood = self.__read('Neighbourhood (choose between these ones, inserting corresponding number):\n'
                                    '1: NERVOSO\n'
                                    '2: MARTENSSONA\n'
                                    '3: MARTENSSONB\n'
                                    '4: MOLICELLEA\n'
                                    '5: MOLICELLEB\n'
                                    '6: MAISONETTES\n'
                                    '7: CHIODO1\n'
                                    '8: CHIODO2\n'
                                    '9: MONACI\n'
                                    '10: SANGENNARO\n', int)
        room_type = self.__read('Room (choose between SINGLE AND DOUBLE):\n'
                                '1: SINGLE\n'
                                '2: DOUBLE\n', int)

        switcherNeigh = {
            1: "NRV",
            2: "MTA",
            3: "MTB",
            4: "MLA",
            5: "MLB",
            6: "MSN",
            7: "CH1",
            8: "CH2",
            9: "MON",
            10: "SNG"
        }

        switcherRoom = {
            1: "SIN",
            2: "DBL"
        }

        return Reservation(switcherNeigh.get(neighbourhood, 'invalid neighbourhood'),
                           switcherRoom.get(room_type, 'invalid room type'))


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
