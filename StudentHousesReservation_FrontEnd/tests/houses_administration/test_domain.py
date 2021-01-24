import pytest
from valid8 import ValidationError

from StudentHousesReservation_FrontEnd.houses_administration.domain import *


def test_apartment_name_format():
    wrong_values = ['', '123', 'AAA', 'AS123', '1A', 'AA1']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Apartment(value)


def test_apartment_str():
    for value in ['A1', 'A11']:
        assert Apartment(value).name == value


def test_admin_correct_values():
    Employee('123456', '12345678910')


def test_admin_wrong_matric_number_format():
    wrong_values = ['AAA', '123', 'A12', '12345', '1234567']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Employee(value, '12345678910')


def test_admin_wrong_password_format():
    wrong_values = ['lessten',  'betweenlenbut!']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Employee('192859', value)


def test_admin_eq():
    ad = Employee('182959', 'ciaobellissimi')
    ad1 = Employee('182959', 'ciaobellissimi')
    ad2 = Employee('182959', 'ciaobellissime')

    assert ad.__eq__(ad1)
    assert not ad.__eq__(ad2)


def test_admin_str():
    ad = Employee('182959', 'ciaobellissimi')
    assert ad.__str__() == '182959 ciaobellissimi'
    assert not ad.__str__() == '182959ciaobellissimi'


def test_student_correct_values():
    Student('123456', '12345678910')


def test_student_wrong_matric_number_format():
    wrong_values = ['AAA', '123', 'A12', '12345', '1234567']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Student(value, '12345678910')


def test_student_wrong_password_format():
    wrong_values = ['lessten', 'betweenlenbut!']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Student('192859', value)


def test_student_equality():
    st = Student('182959', 'ciaobellissimi')
    st1 = Student('182959', 'ciaobellissimi')
    st2 = Student('182959', 'ciaobellissime')

    assert st.__eq__(st1)
    assert not st.__eq__(st2)


def test_student_str():
    st = Student('182959', 'ciaobellissimi')
    assert st.__str__() == '182959 ciaobellissimi'
    assert not st.__str__() == '182959ciaobellissimi'


def test_reservation_neighbho_in_list():
    Reservation('NERVOSO', 'SINGLE')
    wrong_values = ['', 'NERVOSA', '123', '!"dsda', 'nervoso', '1']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Reservation(value, 'SINGLE')


def test_reservation_room_in_list():
    Reservation('NERVOSO', 'SINGLE')
    wrong_values = ['', '1', 'SINGOLA', '!"£SIN34', 'single']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Reservation('NERVOSO', value)


def test_reservation_str():
    re = Reservation('NERVOSO', 'SINGLE')
    assert re.__str__() == 'NERVOSO SINGLE'
    assert not re.__str__() == 'NERVOSA SINGLE'


@pytest.fixture
def admins():
    return [
        Employee('112233', '12345678910'),
        Employee('123456', '1122334455'),
        Employee('111222', '10987654321'),
    ]


@pytest.fixture
def students():
    return [
        Student('112233', '12345678910'),
        Student('123456', '1122334455'),
        Student('111222', '10987654321'),
    ]


@pytest.fixture
def preferences():
    return [
        Reservation('NERVOSO', 'DOUBLE'),
        Reservation('MARTENSSONA', 'SINGLE'),
        Reservation('MOLICELLEA', 'SINGLE'),
    ]


def test_database_add_student(students):
    db = Database()
    size = 0
    for student in students:
        db.add_student(student)
        size += 1
        assert db.students_size() == size
        assert db.student(size - 1) == student


def test_database_add_admin(admins):
    db = Database()
    size = 0
    for admin in admins:
        db.add_admin(admin)
        size += 1
        assert db.admins_size() == size
        assert db.admin(size - 1) == admin


def test_database_add_reservations(students, preferences):
    db = Database()
    size = 0
    keys = range(3)
    for i in keys:
        db.add_reservation(students[i].matriculation_number, preferences[i])
        size += 1
        assert db.number_of_reservations() == size


def test_database_has_already_reservation():
    stud = Student('182959', '12345678910')
    r1 = Reservation('NERVOSO', 'DOUBLE')
    db = Database()
    db.add_reservation(stud.matriculation_number, r1)
    assert db.has_already_reservation(stud.matriculation_number)
    assert not db.has_already_reservation('666777')
    assert db.get_personal_reservation(stud.matriculation_number).__str__() == r1.__str__()


def test_database_validate_wrong_input():
    db = Database()
    s1 = Student('112233', '12345678910')
    s2 = Student('123456', '1122334455')
    s3 = Student('111222', '10987654321')
    a1 = Employee('112233', '12345678910')
    a2 = Employee('123456', '1122334455')
    a3 = Employee('111222', '10987654321')
    r1 = Reservation('NERVOSO', 'DOUBLE')
    r2 = Reservation('MARTENSSONA', 'SINGLE')
    r3 = Reservation('MOLICELLEA', 'SINGLE')
    db.add_student(s1)
    db.add_student(s2)
    db.add_student(s3)
    db.add_admin(a1)
    db.add_admin(a2)
    db.add_admin(a3)
    db.add_reservation(s1.matriculation_number, r1)
    db.add_reservation(s2.matriculation_number, r2)
    db.add_reservation(s3.matriculation_number, r3)

    with pytest.raises(ValidationError):
        db.student(-1)
    with pytest.raises(ValidationError):
        db.student(100)
    with pytest.raises(TypeError):
        db.student('asdsads')

    with pytest.raises(ValidationError):
        db.admin(-1)
    with pytest.raises(ValidationError):
        db.admin(100)
    with pytest.raises(TypeError):
        db.admin('asdsads')

    with pytest.raises(ValidationError):
        db.get_personal_reservation('123')
    with pytest.raises(ValidationError):
        db.get_personal_reservation('123555')
