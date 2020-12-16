from pathlib import Path
from unittest.mock import patch, mock_open, Mock, call

import pytest

from StudentHousesReservation_FrontEnd.houses_administration.app import App, main


@pytest.fixture
def mock_path():
    Path.exists = Mock()
    Path.exists.return_value = True
    return Path


@pytest.fixture
def reservations():
    reservations = [
        ['NERVOSO', 'SINGLE', '223965'],
        ['MARTENSSONA', 'DOUBLE', '223955'],
        ['CHIODO1', 'SINGLE', '223666'],
    ]
    return '\n'.join(['\t'.join(d) for d in reservations])


@pytest.fixture
def students():
    students = [
        ['223965', 'Manuel95.m'],
        ['223955', 'Paolop97.p'],
        ['223963', 'Carlop94.c'],
    ]
    return '\n'.join(['\t'.join(d) for d in students])


@pytest.fixture
def admins():
    admins = [
        ['333965', 'AdmManuel95.m'],
        ['333955', 'AdmPaolop97.p'],
        ['333963', 'AdmCarlop94.c'],
    ]
    return '\n'.join(['\t'.join(d) for d in admins])


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_load_datafile(mocked_print, mocked_input, mock_path, reservations):
    with patch('builtins.open', mock_open(read_data=reservations)):
        App().run()
    mock_path.exists.assert_called_once()
    assert list(filter(lambda x: 'NERVOSO' in str(x), mocked_print.mock_calls))
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='yz')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty list of vehicles...')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_unknown_type_in_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='Airplane\tCA220NE\tFiat\tPunto\t199.99')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty list of vehicles...')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_global_exception_handler(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exits:
        mocked_path_exits.side_effect = Mock(side_effect=Exception('Test'))
        App().run()
    assert mocked_input.mock_calls == []
    assert list(filter(lambda x: 'Panic error!' in str(x), mocked_print.mock_calls))


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    with patch.object(Path, 'exists') as mocked_path_exists:
        mocked_path_exists.return_value = False
        with patch('builtins.open', mock_open()):
            main('__main__')
            mocked_print.assert_any_call('*** LaRusso Auto Group ***')
            mocked_print.assert_any_call('0:\tExit')
            mocked_print.assert_any_call('Bye!')
            mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '0', '0'])
@patch('builtins.print')
def test_app_login_student(mocked_print, mocked_input, mock_path):
    pass


@patch('builtins.input', side_effect=['1', '223885', 'Manuel95.', '0'])
@patch('builtins.print')
def test_app_fail_login_student(mocked_print, mocked_input, mock_path):
    pass


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '1', 'Y', 'NERVOSO', 'SINGLE', '0', '0'])
@patch('builtins.print')
def test_app_add_reservation(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open()) as mocked_open:
        App().run()
    # print(mocked_print)
    # assert list(filter(lambda x: 'CA220NE' in str(x), mocked_print.mock_calls))
    # mocked_print.assert_any_call('1:\tLogin as student')
    # mocked_print.assert_any_call('Matriculation\tNumber:')
    # mocked_print.assert_any_call('Bye!')
    # mocked_input.assert_called()
    handle = mocked_open()
    handle.write.assert_called_once_with('NERVOSO\tSINGLE\t223965')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '2', '0', '0'])
@patch('builtins.print')
def test_app_view_reservation(mocked_print, mocked_input, mock_path):
    pass


@patch('builtins.input', side_effect=['2', '333965', 'AdmManuel95.m', '0', '0'])
@patch('builtins.print')
def test_app_login_admin(mocked_print, mocked_input, mock_path):
    pass


@patch('builtins.input', side_effect=['2', '333969', 'AdmManuel95', '0'])
@patch('builtins.print')
def test_app_fail_login_admin(mocked_print, mocked_input, mock_path):
    pass


@patch('builtins.input', side_effect=['2', '333965', 'AdmManuel95.m', '1', '0', '0'])
@patch('builtins.print')
def test_app_fail_admin_view_reservation(mocked_print, mocked_input, mock_path):
    pass
