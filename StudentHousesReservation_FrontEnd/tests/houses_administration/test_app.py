import sys
from pathlib import Path
from unittest.mock import patch, mock_open, Mock, call

import pytest

from StudentHousesReservation_FrontEnd.houses_administration.app import App, main


def mock_response_dict(status_code, data={}):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


def mock_response(status_code, data=[]):
    res = Mock()
    res.status_code = status_code
    res.json.return_value = data
    return res


# @pytest.fixture
# def mock_path():
#    Path.exists = Mock()
#    Path.exists.return_value = True
#    return Path
#
#
# @pytest.fixture
# def multi_mock_open(*file_contents):
#    mock_files = [mock_open(read_data=content).return_value for content in file_contents]
#    mock_opener = mock_open()
#    mock_opener.side_effect = mock_files
#    return mock_opener
#
#
# @pytest.fixture
# def reservations():
#    reservations = [
#        ['NERVOSO', 'SINGLE', '223965'],
#        ['MARTENSSONA', 'DOUBLE', '223955'],
#        ['CHIODO1', 'SINGLE', '223666'],
#    ]
#    return '\n'.join(['\t'.join(d) for d in reservations])
#
#
# @pytest.fixture
# def students():
#    students = [
#        ['223965', 'd26c7c71c302511fb6d4564db191ef78357796d06da6520411b0f29f17575e7e'],  # pass : 'Manuel95.m'],
#        ['223955', 'd25843dda285d2f190aeabe68d4a72ece38f6398f44d995734d4527190eb4766'],  # pass : 'Paolop97.p'],
#        ['223963', '5ec057110db886a9196dc1d61bbd3a828465227b57c68570c2ad62f417bdbea1'],  # pass : 'Carlop94.c'],
#        ['666777', '222860a94573964a00d861ef18f15e7e328721c325f438f402c92aac9d30a43f'],  # pass : 'Malvi30L.m'],
#    ]
#    return '\n'.join(['\t'.join(d) for d in students])
#
#
# @pytest.fixture
# def employees():
#    employees = [
#        ['333965', 'e2225cbaa0dbb73e7b3351239901b8449612c479a85a66183a9e3d27ef762b79'],  # pass : 'AdmManuel95.m'],
#        ['333955', '81b4dd632617586ad2dcc67ee84dd57956b6b85b283dcddfffa68020cd0f4ca5'],  # pass : 'AdmPaolop97.p'],
#        ['333963', '3cd55af9821debcf053e9219674a7a919a8ed11916c230187cda073138e1f978'],  # pass : 'AdmCarlop94.c'],
#    ]
#    return '\n'.join(['\t'.join(d) for d in employees])
#

# @patch('builtins.input', side_effect=['0'])
# @patch('builtins.print')
# @patch('builtins.open', side_effect=[students, employees, reservations])
# def test_app_load_datafile(mocked_print, mocked_input, mock_path, students, employees, reservations):
#    with patch('builtins.open', mock_open()):
#        App().run()
#    sys.stdout.write(str(mocked_print.call_args_list) + '\n')
#
#    mock_path.exists.call_count == 3
#    mocked_input.assert_called()
#

# @patch('builtins.input', side_effect=['0'])
# @patch('builtins.print')
# def test_app_handles_corrupted_datafile(mocked_print, mocked_input, mock_path):
#    with patch('builtins.open', mock_open(read_data='xyz')):
#        App().run()
#    mocked_print.assert_any_call('Continuing with an empty list of students...')
#    mocked_print.assert_any_call('Continuing with an empty list of employees...')
#    mocked_print.assert_any_call('Continuing with an empty list of reservations...')


# @patch('builtins.input', side_effect=['0'])
# @patch('builtins.print')
# def test_app_global_exception_handler(mocked_print, mocked_input):
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
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')

    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': 'cddb2c3013687d4517ddd7fedbe4b0520510f9f0'})])
@patch('builtins.input', side_effect=['1', '170013', 'manuelito', '0', '0'])
@patch('builtins.print')
def test_app_login_student(mocked_print, mocked_input, mocked_requests_post):
    App().run()
    mocked_requests_post.assert_called_once()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('1:\tLogin as student')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '297da1d55ddd3b75e868dff5b3d574118a33c931'})])
@patch('builtins.input', side_effect=['2', 'signorasara', 'formaggio', '0', '0'])
@patch('builtins.print')
def test_app_login_employee(mocked_print, mocked_input, mocked_requests_post):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as employee')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Administration panel ***')
    mocked_print.assert_any_call('1:\tShow all required reservations')
    mocked_print.assert_any_call('Bye!')
    mocked_requests_post.assert_called_once()
    mocked_input.assert_called()


@patch('requests.get', side_effect=[])
@patch('builtins.input', side_effect=['1', '170013', 'manuelito'])
@patch('builtins.print')
def test_app_panic_error(mocked_print, mocked_input,mocked_requests_get):
    App().run()
    sys.stdout.write(str(mocked_print.call_args_list) + '\n')
    assert list(filter(lambda x: 'Panic error!' in str(x), mocked_print.mock_calls))


@patch('requests.post',
       side_effect=[mock_response_dict(200, {'key': '297da1d55ddd3b75e868dff5b3d574118a33c931'}), mock_response(400),
                    mock_response(201)])
@patch('requests.get', side_effect=[mock_response(200), mock_response(200)])
@patch('builtins.input', side_effect=['1', '170013', 'manuelito', '1', '1', '1', '1', '1', '1', '0', '0'])
@patch('builtins.print')
def test_app_student_add_first_reservation(mocked_print, mocked_input, mocked_requests_post, mocked_requests_get):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Something went wrong with reservation adding')
    mocked_print.assert_any_call('Reservation successfully added')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post',
       side_effect=[mock_response_dict(200, {'key': '297da1d55ddd3b75e868dff5b3d574118a33c931'})])
@patch('requests.get', side_effect=[mock_response(200, [{"id": "1", "neighborhood": "NRV", "room_type": "SIN"}]),
                                    mock_response(200, [{"id": "1", "neighborhood": "NRV", "room_type": "SIN"}]),
                                    mock_response(200, [{"id": "1", "neighborhood": "NRV", "room_type": "SIN"}]),
                                    mock_response(200, [{"id": "1", "neighborhood": "NRV", "room_type": "SIN"}]),
                                    mock_response(200, [{"id": "1", "neighborhood": "NRV", "room_type": "SIN"}])
                                    ])
@patch('builtins.input', side_effect=['1', '170013', 'manuelito',
                                      '1', '1', '1', 'd',
                                      '1', '1', '1', 'n',
                                      '1', '1', '1', 'N',
                                      '1', '1', '1', 'Y',
                                      '1', '1', '1', 'Y',
                                      '0', '0'])
@patch('requests.patch', side_effect=[mock_response_dict(400), mock_response_dict(200)])
@patch('builtins.print')
def test_app_student_fails_to_add_first_reservation(mocked_print, mocked_input, mocked_requests_post,
                                                    mocked_requests_get, mocked_requests_patch):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')
    mocked_print.assert_any_call('Your new preferences will overwrite the previous ones, do you now? Y/N')
    mocked_print.assert_any_call('I, lets go!')
    assert len(list(filter(lambda
                               x: 'Invalid key entered, please choose to add a new reservation and retry with a '
                                  'correct one...' in str(x), mocked_print.mock_calls))) == 2
    assert len(list(filter(lambda
                               x: 'Your new preferences will overwrite the previous ones, do you now? Y/N' in str(x),
                           mocked_print.mock_calls))) == 5
    mocked_print.assert_any_call('Reservation successfully updated')
    mocked_print.assert_any_call('Something went wrong with reservation updating...')
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post', side_effect=[mock_response_dict(200, {'key': '297da1d55ddd3b75e868dff5b3d574118a33c931'})])
@patch('requests.get', side_effect=[mock_response(200), mock_response(200), mock_response(200)])
@patch('builtins.input',
       side_effect=['1', '170013', 'manuelito', '1', '12', '1', '1', '0', '1', '1', 'asd', '1', '5', '0', '0'])
@patch('builtins.print')
def test_app_student_wrong_reservation_added_wrong_format(mocked_print, mocked_input, mocked_requests_post,
                                                          mocked_requests_get):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    assert len(list(filter(lambda
                               x: 'invalid literal' in str(
        x), mocked_print.mock_calls))) == 1
    assert len(list(filter(lambda
                               x: 'Invalid key entered, please choose to add a new reservation and retry with a '
                                  'correct one...' in str(x), mocked_print.mock_calls))) == 3
    mocked_print.assert_any_call('Successfully logged out from the system!')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')


@patch('requests.post',
       side_effect=[mock_response_dict(200, {'key': 'cddb2c3013687d4517ddd7fedbe4b0520510f9f0'}), mock_response(201)])
@patch('requests.get',
       side_effect=[mock_response(200), mock_response(200, [{"neighborhood": "NRV", "room_type": "SIN"}])])
@patch('builtins.input',
       side_effect=['1', '170013', 'manuelito', '1', '1', '1', '2', '0', '0'])
@patch('builtins.print')
def test_app_student_view_his_reservation_after_adding(mocked_print, mocked_input, mocked_requests_post,
                                                       mocked_requests_get):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('Reservation successfully added')
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')
    assert list(filter(lambda x: 'NRV' in str(x), mocked_print.mock_calls))
    assert list(filter(lambda x: 'SIN' in str(x), mocked_print.mock_calls))
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post',
       side_effect=[mock_response_dict(200, {'key': 'cddb2c3013687d4517ddd7fedbe4b0520510f9f0'}), mock_response(201)])
@patch('requests.get',
       side_effect=[mock_response(200), mock_response(400)])
@patch('builtins.input',
       side_effect=['1', '170013', 'manuelito', '1', '1', '1', '2', '0', '0'])
@patch('builtins.print')
def test_app_student_fail_to_view_his_reservation_after_adding(mocked_print, mocked_input, mocked_requests_post,
                                                               mocked_requests_get):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')
    mocked_print.assert_any_call('Something went wrong with your request: RIPIT')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post',
       side_effect=[mock_response_dict(200, {'key': 'cddb2c3013687d4517ddd7fedbe4b0520510f9f0'}), mock_response(201)])
@patch('requests.get', side_effect=[mock_response(200)])
@patch('builtins.input',
       side_effect=['1', '170013', 'manuelito', '2', '0', '0'])
@patch('builtins.print')
def test_app_student_has_no_reservation(mocked_print, mocked_input, mocked_requests_post,
                                        mocked_requests_get):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('0:\tExit')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Students panel ***')
    mocked_print.assert_any_call('No reservation found for your matriculation number')
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post',
       side_effect=[mock_response_dict(200, {'key': '297da1d55ddd3b75e868dff5b3d574118a33c931'})])
@patch('requests.get', side_effect=[mock_response(200, [
    {"neighborhood": "NRV", "room_type": "SIN", "user": "1"},
    {"neighborhood": "MTB", "room_type": "DBL", "user": "2"},
    {"neighborhood": "CH2", "room_type": "SIN", "user": "3"}])])
@patch('builtins.input', side_effect=['2', 'signorasara', 'formaggio', '1', '0', '0'])
@patch('builtins.print')
def test_app_employee_view_all_reservation(mocked_print, mocked_input, mocked_requests_post,
                                           mocked_requests_get):
    App().run()
    # sys.stdout.write(str(mocked_print.call_args_list) + '\n')

    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as employee')
    mocked_print.assert_any_call('SUCCESSFUL LOGIN')
    mocked_print.assert_any_call('*** Administration panel ***')
    mocked_print.assert_any_call('1:\tShow all required reservations')

    assert list(filter(lambda x: 'NRV' in str(x), mocked_print.mock_calls))
    assert list(filter(lambda x: 'MTB' in str(x), mocked_print.mock_calls))
    assert list(filter(lambda x: 'CH2' in str(x), mocked_print.mock_calls))
    assert list(filter(lambda x: 'DBL' in str(x), mocked_print.mock_calls))
    assert list(filter(lambda x: 'NRV' in str(x), mocked_print.mock_calls))
    assert len(list(filter(lambda x: 'SIN' in str(x), mocked_print.mock_calls))) == 2
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['1', '123', 'FSAFAS', '0'])
@patch('builtins.print')
def test_app_fail_login_student_wrong_format(mocked_print, mocked_input, ):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('1:\tLogin as student')
    mocked_print.assert_any_call('Access failed: please, choose to login and retry with correctly typed credentials...')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['2', 'morethanfifteenchar', 'FSAFAS', '0'])
@patch('builtins.print')
def test_app_fail_login_employee_wrong_format(mocked_print, mocked_input):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as employee')
    mocked_print.assert_any_call('Access failed: please, choose to login and retry with correct credentials...')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post',
       side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['1', '123456', 'password', '0'])
@patch('builtins.print')
def test_app_fail_login_student_correct_format(mocked_print, mocked_input, mocked_requests_post):
    App().run()
    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('1:\tLogin as student')
    mocked_print.assert_any_call('No account found with these credentials')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('requests.post',
       side_effect=[mock_response_dict(400)])
@patch('builtins.input', side_effect=['2', 'username', 'password', '0'])
@patch('builtins.print')
def test_app_fail_login_employee_correct_format(mocked_print, mocked_input, mocked_requests_post):
    App().run()

    mocked_print.assert_any_call('*** Student houses reservations platform ***')
    mocked_print.assert_any_call('2:\tLogin as employee')
    mocked_print.assert_any_call('No account found with these credentials')
    mocked_print.assert_any_call('Bye!')
    mocked_input.assert_called()


@patch('builtins.input', side_effect=['', '11', 'aas', '0'])
@patch('builtins.print')
def test_app_wrong_entry(mocked_print, mocked_input):
    App().run()
    mocked_print.assert_any_call('Invalid selection. Please, try again...')
    sys.stdout.write(str(mocked_input.call_args_list) + '\n')
    assert mocked_input.call_count == 4  # 3 request answered with errors + 1 with 0
    assert len(list(filter(lambda x: 'Invalid selection. Please, try again..' in str(x), mocked_print.mock_calls))) == 3
