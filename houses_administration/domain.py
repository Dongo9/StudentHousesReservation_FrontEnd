from dataclasses import dataclass, field
from enum import Enum
from typing import List

from typeguard import typechecked
from valid8 import validate

from StudentHousesReservation_FrontEnd.validation.dataclasses import validate_dataclass

from StudentHousesReservation_FrontEnd.validation.regex import pattern


class RoomType(Enum):
    SINGLE = 1
    DOUBLE = 2


class NeighbourhoodName(Enum):
    NERVOSO = 'Nervoso',
    MARTENSSON_A = 'MartenssonA',
    MARTENSSON_B = 'MartenssonB',
    MOLICELLE_A = 'MolicelleA',
    MOLICELLE_B = 'MolicelleB',
    MAISONETTES = 'Maisonettes',
    CHIODO_1 = 'Chiodo1',
    CHIODO_2 = 'Chiodo2',
    MONACI = 'Monaci',
    SAN_GENNARO = 'SanGennaro',


@typechecked
@dataclass(frozen=True, order=True)
class Student:
    matriculation_number: int
    name: str
    surname: str
    is_beneficiary: bool

    def __post_init__(self):
        validate_dataclass(self)
        validate('matriculation_number', self.matriculation_number, min_len=6, max_len=6, custom=pattern(r'[0-9]{6}'))
        validate('name', self.name, min_len=3, max_len=15, custom_name=pattern(r'[A-Za-z\s]+'))
        validate('surname', self.surname, min_len=3, max_len=25, custom_name=pattern(r'[A-Za-z\s]+'))

    def __str__(self):
        return 'matriculation number:' + self.matriculation_number + '  student name: ' + self.name + ' ' + self.surname


@typechecked
@dataclass(frozen=True, order=True)
class Bed:

    room_number: int
    bed_number: int
    room_type: RoomType
    has_private_bathroom: bool
    student: Student = None #DOVREBBE ESSERE LECITO

    def __post_init__(self):
        validate_dataclass(self)
        validate('room_number', self.room_number, min_len=1, max_len=1, custom=pattern(r'[1-6]'))
        validate('bed_number', self.bed_number, min_len=1, max_len=1, custom=pattern(r'[1-2]'))

    def __str__(self):
        return 'Room number: ' + self.room_number + '  n. of beds' + self.bed_number + '  type of room' + self.room_type


@typechecked
@dataclass(frozen=True, order=True)
class Apartment:
    id: str
    bathrooms_number: int
    couches_number: int
    armchairs_number: int
    floor: int

    __beds: List[Bed] = field(default_factory=list, init=False)

    def __post_init__(self):
        validate_dataclass(self)
        validate('id', self.id, min_len=2, max_len=3, custom=pattern(r'[A-Z][1-9]{1,2}'))
        validate('bathrooms_number', self.bathrooms_number, min_len=1, max_len=1, custom=pattern(r'[1-6]'))
        validate('armachairs_number', self.armchairs_number, min_len=1, max_len=1, custom=pattern(r'[1-3]'))
        validate('floor', self.floor, min_len=1, max_len=1, pattern=r'[0-6]')

    def beds(self) -> int:
        return len(self.__beds)

    def bed(self, index: int) -> Bed:
        validate('index', index, min_value=0, max_value=self.beds() - 1)
        return self.__beds[index]

    def __str__(self):
        return self.id + ' ' + '  n. of bathrooms: ' + self.bathrooms_number \
               + '  n. of couches: ' + self.couches_number \
               + '  n. of sofas: ' + self.armchairs_number \
               + '  floor: ' + self.floor


@typechecked
@dataclass(frozen=True, order=True)
class Neighbourhood:
    name: NeighbourhoodName

    __apartments: List[Apartment] = field(default_factory=list, init=False)  # RIGUARDARE L'INIT

    def __post_init__(self):
        validate_dataclass(self)

    def apartments(self) -> int: #RITORNA NUMERO DI APPARTAMENTI NEL QUARTIERE
        return len(self.__apartments)

    def apartment(self, index: int) -> Apartment: #RITORNA APPARTAMENTO X IN UN QUARTIERE
        validate('index', index, min_value=0, max_value=self.apartments() - 1)
        return self.__apartments[index]

    def __str__(self):
        return 'Neighbourhood name: ' + self.name
