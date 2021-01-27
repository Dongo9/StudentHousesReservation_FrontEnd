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
def test_app_panic_error(mocked_print, mocked_input, mocked_requests_get):
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
                               x: 'Invalid keys entered: please, choose to add a new reservation and retry with '
                                  'correct ones'
                                  in str(x), mocked_print.mock_calls))) == 3
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
