import requests
from faker import Faker

"""
1. Test data creation : data_for_api_end_points
2. Expected Response Creation :
3. Executing Requests
4. Assertion between expected response & api response by previous
"""

BASE_URL = "http://localhost:8000"

def data_for_api_end_points():
    post_data = None
    test_data = Faker()

    user_id = 'user_' + str(test_data.random_number(digits=5))
    exist_user_id = user_id
    name = test_data.name()
    update_name = test_data.name()
    username = test_data.user_name()
    password = test_data.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    email = test_data.email()
    update_email = test_data.email()

    post_data = {'user_id': user_id, 'name': name, 'username': username, 'password': password, 'email': email}
    put_data = {'user_id': user_id, 'name': update_name, 'email': update_email}
    delete_data = {'user_id': user_id}

    return post_data, put_data, delete_data

def expected_response_creator(request_type='GET', payload_data=None, test_case_type='POSITIVE', expected_message=None):

    expected_response = payload_data

    if request_type == 'GET' and  test_case_type == 'NEGATIVE':
        return expected_message
    elif test_case_type == 'POSITIVE':
        expected_response['status'] = 'success'
    elif test_case_type == 'NEGATIVE':
        expected_response['status'] = 'error'
    else:
        print("Suppported Test Case Types are POSITIVE, NEGATIVE. Raise Future Request for additional types...")

    expected_response['message'] = expected_message

    return expected_response

def request_handler_and_verfier(end_point_url=None, request_type='GET', payload_data=None, expected_response=None,
                    expected_response_status_code=None):

    response = None

    try:
        if request_type == 'POST':
            response = requests.post(f"{BASE_URL}/{end_point_url}", json=payload_data)
        elif request_type == 'GET':
            response = requests.get(f"{BASE_URL}/{end_point_url}/{payload_data['user_id']}")
        elif request_type == 'PUT':
            response = requests.put(f"{BASE_URL}/{end_point_url}/{payload_data['user_id']}", json=payload_data)
        elif request_type == 'DELETE':
            response = requests.delete(f"{BASE_URL}/{end_point_url}/{payload_data['user_id']}")
        else:
            print("Suppported End Point Request Types are POST, GET, PUT, DELETE. Raise Future Request for additional types...")
    except Exception as err:
        assert False, f"{request_type} request for url {end_point_url} is failing due exception with message : {err}"

    print(response.json())
    print(expected_response)
    print(response.status_code)

    if expected_response_status_code is None:
        assert response.status_code == 200
    else:
        assert response.status_code == expected_response_status_code

    if request_type == 'GET':
        for key, value in expected_response.items():
            if key != 'password':
                assert expected_response[key] == response.json()[key]
    else:
        assert response.json()      == expected_response


