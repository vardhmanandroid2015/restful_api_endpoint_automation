import pytest
from .utilities import *
import json

post_data, put_data, delete_data = data_for_api_end_points()

@pytest.mark.parametrize("request_type, end_point_url, test_case_type, expected_message",
                         [('POST', 'create_users', 'POSITIVE', 'User is created'),
                          ('POST', 'create_users', 'NEGATIVE', 'Requested user_id is already exist'),
                          ('GET', 'users', 'POSITIVE', 'User data is fetched without any issue'),
                          ('GET', 'users', 'NEGATIVE', "{'detail': 'User not found'}"),])
def test_generic_post_create_user(request_type, end_point_url, test_case_type, expected_message):

    expected_response_status_code = None

    expected_response = expected_response_creator(request_type=request_type, payload_data=post_data,
                              test_case_type=test_case_type, expected_message=expected_message)


    if test_case_type == 'NEGATIVE':
        if request_type != 'POST':
            post_data['user_id'] = 'NonExistUser123'
        if request_type == 'GET':
            expected_response_status_code = 404

    request_handler_and_verfier(end_point_url=end_point_url, request_type=request_type,
                                payload_data=post_data, expected_response=expected_response,
                                expected_response_status_code=expected_response_status_code)

# def test_generic_put_update_exist_user():
#
#     expected_response = expected_response_creator(request_type='PUT', payload_data=put_data,
#                               test_case_type='POSITIVE', expected_message='User data is updated without any issue')
#
#     request_handler(end_point_url='users', request_type='PUT',
#                     payload_data=put_data, expected_response=expected_response)
#
# def test_generic_put_update_non_exist_user():
#     put_data['user_id'] = 'NonExistUser123'
#
#     expected_response = expected_response_creator(request_type='PUT', payload_data=put_data,
#                               test_case_type='NEGATIVE', expected_message='User not Found')
#
#     request_handler(end_point_url='users', request_type='PUT',
#                     payload_data=put_data, expected_response=expected_response)
#
# def test_generic_delete_exist_user():
#
#
#     expected_response = expected_response_creator(request_type='DELETE', payload_data=delete_data,
#                               test_case_type='POSITIVE', expected_message='User deleted successfully')
#
#     request_handler(end_point_url='users', request_type='DELETE',
#                     payload_data=delete_data, expected_response=expected_response)
#
# def test_generic_delete_non_exist_user():
#
#     delete_data['user_id'] = 'NonExistUser123'
#
#     expected_response = expected_response_creator(request_type='DELETE', payload_data=delete_data,
#                               test_case_type='NEGATIVE', expected_message='User not found')
#
#     request_handler(end_point_url='users', request_type='DELETE',
#                     payload_data=delete_data, expected_response=expected_response)