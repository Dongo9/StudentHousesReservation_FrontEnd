import pytest
from valid8 import ValidationError

from StudentHousesReservation_FrontEnd.houses_administration.domain import *


def test_employee_correct_values():
    Employee('signorasara', 'arrivederci1.')


def test_employee_wrong_matric_number_format():
    wrong_values = ['AA', '13', 'A2', '12345<!', '123456']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Employee(value, '12345678910')


def test_admin_wrong_password_format():
    wrong_values = ['lessten', 'betweenlenbut!']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Employee('192859', value)


def test_employee_eq():
    ad = Employee('turuzzu', 'ciaobellissimi')
    ad1 = Employee('turuzzu', 'ciaobellissimi')
    ad2 = Employee('turuzzi', 'ciaobellissime')

    assert ad.__eq__(ad1)
    assert not ad.__eq__(ad2)


def test_employee_str():
    ad = Employee('1829595', 'ciaobellissimi')
    assert ad.__str__() == '1829595 ciaobellissimi'
    assert not ad.__str__() == '1829595ciaobellissimi'


def test_student_correct_values():
    Student('123456', '12345678910')


def test_student_wrong_matric_number_format():
    wrong_values = ['AAA', '123', 'A12', '12345', '1234567']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Student(value, '12345678910')


def test_student_wrong_password_format():
    wrong_values = ['less', 'betweenlenbut!1234567']
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
    Reservation('NRV', 'SIN')
    wrong_values = ['', 'NERVOSA', '123', '!"dsda', 'nervoso', '1']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Reservation(value, 'SINGLE')


def test_reservation_room_in_list():
    Reservation('NRV', 'SIN')
    wrong_values = ['', '1', 'SINGOLA', '!"£SIN34', 'single']
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Reservation('NRV', value)


def test_reservation_str():
    re = Reservation('NRV', 'SIN')
    assert re.__str__() == 'NRV SIN'
    assert not re.__str__() == 'NRVA SIN'