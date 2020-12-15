from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict

from typeguard import typechecked
from valid8 import validate

from StudentHousesReservation_FrontEnd.validation.dataclasses import validate_dataclass
from StudentHousesReservation_FrontEnd.validation.regex import pattern


class Room(Enum):
    SINGLE = 'SINGLE'
    DOUBLE = 'DOUBLE'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class Neighbourhood(Enum):
    NERVOSO = 'NERVOSO'
    MARTENSSONA = 'MARTENSSONA'
    MARTENSSONB = 'MARTENSSONB'
    MOLICELLEA = 'MOLICELLEA'
    MOLICELLEB = 'MOLICELLEB'
    MAISONETTES = 'MAISONETTES'
    CHIODO1 = 'CHIODO1'
    CHIODO2 = 'CHIODO2'
    MONACI = 'MONACI'
    SANGENNARO = 'SANGENNARO'

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


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
class Admin:
    matriculation_number: str
    password: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('matriculation_number', self.matriculation_number, min_len=6, max_len=6, custom=pattern(r'[0-9]+'))
        validate('password', self.password, min_len=10, max_len=15, custom=pattern(r'[A-Za-z.0-9]+'))

    def __str__(self):
        return self.matriculation_number + ' ' + self.password

    def __eq__(self, other):
        if self.matriculation_number == other.matriculation_number and self.password == other.password:
            return True
        return False


@typechecked
@dataclass(frozen=True, order=True)
class Student:
    matriculation_number: str
    password: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('matriculation_number', self.matriculation_number, min_len=6, max_len=6, custom=pattern(r'[0-9]+'))
        validate('password', self.password, min_len=10, max_len=15, custom=pattern(r'[A-Za-z.0-9]+'))

    def __str__(self):
        return self.matriculation_number + ' ' + self.password

    def __eq__(self, other):
        if self.matriculation_number == other.matriculation_number and self.password == other.password:
            return True
        return False


@typechecked
@dataclass(frozen=True, order=True)
class Reservation:
    neighbourhood: str
    room: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('neighbourhood', self.neighbourhood, is_in=Neighbourhood.__members__)
        validate('room_type', self.room, is_in=Room.__members__)

    def __str__(self):
        return self.neighbourhood + ' ' + self.room


@typechecked
@dataclass(frozen=True)
class Database:
    __reservations: Dict[str, Reservation] = field(default_factory=dict, repr=False, init=False)

    __students: List[Student] = field(default_factory=list, init=False)

    __admins: List[Admin] = field(default_factory=list, init=False)

    def number_of_reservations(self) -> int:
        return len(self.__reservations)

    def reservations(self) -> Dict[str, Reservation]:
        return self.__reservations.copy()  # PER EVITARE MANOMISSIONI ESTERNE (COME CLONE IN JAVA)

    def has_already_reservation(self, stud: str) -> bool:
        if stud in self.__reservations:
            return True
        return False

    def get_personal_reservation(self, matriculation: str) -> Reservation:
        validate('matriculation', matriculation, is_in=self.__reservations)
        return self.__reservations[matriculation]

    def add_reservation(self, stud: str, res: Reservation) -> None:
        self.__reservations[stud] = res

    def add_student(self, stud: Student) -> None:
        self.__students.append(stud)

    def students_size(self) -> int:
        return len(self.__students)

    def student(self, index: int) -> Student:
        validate('index', index, min_value=0, max_value=self.students_size() - 1)
        return self.__students[index]

    def add_admin(self, adm: Admin) -> None:
        self.__admins.append(adm)

    def admins_size(self) -> int:
        return len(self.__admins)

    def admin(self, index: int) -> Admin:
        validate('index', index, min_value=0, max_value=self.admins_size() - 1)
        return self.__admins[index]