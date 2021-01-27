from dataclasses import dataclass
from enum import Enum

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
class Employee:
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
        if self.matriculation_number == other.matriculation_number and self.password == other.password:
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
