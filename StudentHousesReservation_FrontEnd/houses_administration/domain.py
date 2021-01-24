from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

from typeguard import typechecked
from valid8 import validate

from StudentHousesReservation_FrontEnd.validation.dataclasses import validate_dataclass
from StudentHousesReservation_FrontEnd.validation.regex import pattern


class Room(Enum): #ENUM CONTENENTE I VARI TIPI DI STANZA
    SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'


class Neighbourhood(Enum): #ENUM CONTENENTE I VARI QUARTIERI DISPONIBILI
    NERVOSO = 'NRV'
    MARTENSSONA = 'MTA'
    MARTENSSONB = 'MTB'
    MOLICELLEA = 'MLA'
    MOLICELLEB = 'MLB'
    MAISONETTES = 'MSN'
    CHIODO1 = 'CH1'
    CHIODO2 = 'CH2'
    MONACI = 'MON'
    SANGENNARO = 'SNG'


@typechecked
@dataclass(frozen=True, order=True)
class Apartment:
    name: str
    rooms: List[Room] = field(default_factory=list, init=False)

    def __post_init__(self):
        validate_dataclass(self)
        validate('name', self.name, min_len=2, max_len=3, custom=pattern(r'[A-Z][1-9]{1,2}'))


@typechecked
@dataclass(frozen=True, order=True)
class Employee: #CLASSE ADMIN #TODO RINOMINARE IN EMPLOYEE
    username: str
    password: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('username', self.username, min_len=3, max_len=15, custom=pattern(r'(?!(^[0-9]{6}$))([A-Za-z0-9]+)'))
        validate('password', self.password, min_len=5, max_len=15, custom=pattern(r'[A-Za-z.0-9]+'))

    def __str__(self):
        return self.username + ' ' + self.password

    def __eq__(self, other):
        if self.username == other.username and self.password == other.password:
            return True
        return False


@typechecked
@dataclass(frozen=True, order=True)
class Student: #CLASSE STUDENT
    matriculation_number: str
    password: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('matriculation_number', self.matriculation_number, min_len=6, max_len=6, custom=pattern(r'[0-9]+'))
        validate('password', self.password, min_len=5, max_len=15, custom=pattern(r'[A-Za-z.0-9]+'))

    def __str__(self):
        return self.matriculation_number + ' ' + self.password

    def __eq__(self, other):
        if self.matriculation_number == other.username and self.password == other.password:
            return True
        return False


@typechecked
@dataclass(frozen=True, order=True)
class Reservation: #CLASSE RESERVATION
    neighbourhood: str
    room: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('neighbourhood', self.neighbourhood, is_in={'NRV', 'MTA', 'MTB', 'MLA', 'MLB', 'MSN', 'CH1', 'CH2', 'MON', 'SNG'})
        validate('room_type', self.room, is_in={'SIN', 'DBL'})

    def __str__(self):
        return self.neighbourhood + ' ' + self.room


@typechecked
@dataclass(frozen=True)
class Database:
    __reservations: Dict[str, Reservation] = field(default_factory=dict, repr=False, init=False) #DICTIONARY PER LE RESERVATIONS

    __students: List[Student] = field(default_factory=list, init=False) #LISTA PER GLI STUDENTI

    __admins: List[Employee] = field(default_factory=list, init=False) #LISTA PER GLI ADMINS

    def number_of_reservations(self) -> int:
        return len(self.__reservations)

    def students_size(self) -> int:
        return len(self.__students)

    def admins_size(self) -> int:
        return len(self.__admins)

    def add_reservation(self, stud: str, res: Reservation) -> None:
        self.__reservations[stud] = res

    def add_student(self, stud: Student) -> None:
        self.__students.append(stud)

    def add_admin(self, adm: Employee) -> None:
        self.__admins.append(adm)

    def reservations(self) -> Dict[str, Reservation]:
        return self.__reservations.copy()  # PER EVITARE MANOMISSIONI ESTERNE (COME CLONE IN JAVA)

    def student(self, index: int) -> Student:
        validate('index', index, min_value=0, max_value=self.students_size() - 1)
        return self.__students[index]

    def admin(self, index: int) -> Employee:
        validate('index', index, min_value=0, max_value=self.admins_size() - 1)
        return self.__admins[index]

    def has_already_reservation(self, stud: str) -> bool:
        if stud in self.__reservations:
            return True
        return False

    def get_personal_reservation(self, matriculation: str) -> Reservation:
        validate('matriculation', matriculation, is_in=self.__reservations)
        return self.__reservations[matriculation]

    def check_credentials(self, stud: Student) -> bool:
        for i in range(self.students_size()):  # CHECK SULLA CORRISPONDENZA TRA I VARI STUDENTI
            st = self.student(i)
            if st.__eq__(stud):
                return True
        return False

    def check_admin_credentials(self, admin: Employee) -> bool: #EQUIVALENTE DI STUDENTE
        for i in range(self.admins_size()):
            ad = self.admin(i)
            if ad.__eq__(admin):
                return True
        return False
