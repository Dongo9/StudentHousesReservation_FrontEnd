import sys
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
def multi_mock_open(*file_contents):
    mock_files = [mock_open(read_data=content).return_value for content in file_contents]
    mock_opener = mock_open()
    mock_opener.side_effect = mock_files
    return mock_opener


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
        ['666777', 'Malvi30L.m'],
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
@patch('builtins.open', side_effect=[students, admins, reservations])
def test_app_load_datafile(mocked_print, mocked_input, mock_path, students, admins, reservations):
    with patch('builtins.open', mock_open()):
        App().run()
    sys.stdout.write(str(mocked_print.call_args_list) + '\n')

    mock_path.exists.call_count == 3
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
    with patch('builtins.open', mock_open(read_data='xyz')):
        App().run()
    mocked_print.assert_any_call('Continuing with an empty list of students...')
    mocked_print.assert_any_call('Continuing with an empty list of admins...')
    mocked_print.assert_any_call('Continuing with an empty list of reservations...')
    mocked_input.assert_called()


#@patch('builtins.input', side_effect=['0'])
#@patch('builtins.print')
#def test_app_global_exception_handler(mocked_print, mocked_input):
#    with patch.object(Path, 'exists') as mocked_path_exits:
#        mocked_path_exits.side_effect = Mock(side_effect=Exception('Test'))
#        App().run()
#    sys.stdout.write(str(mocked_print.call_args_list) + '\n')
#    assert mocked_input.mock_calls == []
#    assert list(filter(lambda x: 'Panic error!' in str(x), mocked_print.mock_calls))


@patch('builtins.input', side_effect=['0'])
@patch('builtins.print')
def test_app_main(mocked_print, mocked_input):
    main('__main__')
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '0', '0'])
@patch('builtins.print')
def test_app_login_student(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('1:\tLogin as student')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', '333965', 'AdmManuel95.m', '0', '0'])
@patch('builtins.print')
def test_app_login_admin(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as administrator')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Administration panel ***')
    mocked_print.assert_any_call('1:\tShow all required reservations')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '1', 'N', '1', 'Y', 'NERVOSO', 'SINGLE', '0', '0'])
@patch('builtins.print')
def test_app_student_add_reservation(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Your new preferences will overwrite the previous ones, do you now? Y/N')
    mocked_print.assert_any_call('Reservation added')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    ####CONTROLLARE SE E' STATA AGGIUNTA
    # handle = mocked_open()
    # handle.write.assert_called_once_with('Moto\tCA220NI\tKawasaki\tNinja\t1000.00\n')
    mocked_input.assert_called()


@patch('builtins.input',
       side_effect=['1', '223965', 'Manuel95.m', '1', 'Y', 'FAKE', 'SINGLE', '1', 'Y', 'NERVOSO', 'FAKE', '1', 'Y',
                    'FAKEUNO', 'FAKEDUE', '0', '0'])
@patch('builtins.print')
def test_app_student_wrong_reservation_added_wrong_format(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Your new preferences will overwrite the previous ones, do you now? Y/N')
    assert len(list(filter(lambda
                               x: 'Wrong values entered: please, choose to add a new reservation and retry with correct values...' in str(
        x), mocked_print.mock_calls))) == 3
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '2', '0', '0'])
@patch('builtins.print')
def test_app_student_view_his_reservation(mocked_print, mocked_input, mock_path, reservations):
    # with patch('builtins.open', mock_open(read_data=reservations)):
    #    App().run()
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Students panel ***')
    # assert list(filter(lambda x: 'NERVOSO' in str(x), mocked_print.mock_calls))
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()

@patch('builtins.input', side_effect=['1', '666777', 'Malvi30L.m', '2', '0', '0'])
@patch('builtins.print')
def test_app_student_has_no_reservation(mocked_print, mocked_input, mock_path, reservations):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('No reservation found for your matriculation number')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()

@patch('builtins.input', side_effect=['2', '333965', 'AdmManuel95.m', '1', '0', '0'])
@patch('builtins.print')
#@patch('builtins.open', side_effect=[students, admins, reservations])
def test_app_admin_view_all_reservation(mocked_print, mocked_input, mock_path, students, admins, reservations):
    #with patch('builtins.open', mock_open()):
    App().run()
    #sys.stdout.write(str(mocked_print.call_args_list) + '\n')

    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as administrator')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Administration panel ***')
    mocked_print.assert_any_call('1:\tShow all required reservations')
    assert list(filter(lambda x: 'NERVOSO' in str(x), mocked_print.mock_calls))
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '123', 'FSAFAS', '0'])
@patch('builtins.print')
def test_app_fail_login_student_wrong_format(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('1:\tLogin as student')
    mocked_print.assert_any_call('Access failed: please, choose to login and retry with correct credentials...')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', '123', 'FSAFAS', '0'])
@patch('builtins.print')
def test_app_fail_login_admin_wrong_format(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as administrator')
    mocked_print.assert_any_call('Access failed: please, choose to login and retry with correct credentials...')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '123456', 'ciaobellissimi', '0'])
@patch('builtins.print')
def test_app_fail_login_student_correct_format(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('1:\tLogin as student')
    mocked_print.assert_any_call('No account found with this credentials')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', '123456', 'ciaobellissimi', '0'])
@patch('builtins.print')
def test_app_fail_login_admin_correct_format(mocked_print, mocked_input, mock_path):
    App().run()

    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as administrator')
    mocked_print.assert_any_call('No account found with this credentials')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['', '11', 'aas', '0'])
@patch('builtins.print')
def test_app_wrong_entry(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('Invalid selection. Please, try again...')
    sys.stdout.write(str(mocked_input.call_args_list) + '\n')
    assert mocked_input.call_count == 4  # 3 request answered with errors + 1 with 0
    assert len(list(filter(lambda x: 'Invalid selection. Please, try again..' in str(x), mocked_print.mock_calls))) == 3


@patch('builtins.input', side_effect=['1', '223965', 'Manuel95.m', '1', '', '1', '2', '1', 'FAKE', '0', '0'])
@patch('builtins.print')
def test_app_possible_wrong_key_entry(mocked_print, mocked_input, mock_path):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Successful login')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Your new preferences will overwrite the previous ones, do you now? Y/N')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    assert len(list(filter(lambda
                               x: 'Invalid key entered, please choose to add a new reservation and retry with a correct one...' in str(
        x), mocked_print.mock_calls))) == 3
    mocked_input.assert_called()
