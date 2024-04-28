import requests
from faker import Faker

# URL for web server
BASE_URL = f"http://localhost:8000"
  # - create_user
  # - users/{user_id}

test_data = Faker()

user_id = 'user_' + str(test_data.random_number(digits=5))
name = test_data.name()
update_name = test_data.name()
username = test_data.user_name()
password = test_data.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
email = test_data.email()
update_email = test_data.email()

def test_post_request_to_create_user():
    post_data_to_create_user = {'user_id': user_id, 'name': name, 'username': username, 'password': password, 'email': email}

    expected_response_data = {'user_id': user_id, 'name': name, 'username': username, 'password': password,
                              'email': email, 'status': 'success', 'message': 'User is created'}

    try:
        response = requests.post(f"{BASE_URL}/create_users", json=post_data_to_create_user)
        assert response.status_code == 200
    except Exception as err:
        print(err)
        assert False, f"POST request is failing due exception with message : {err}"

    expected_response_data = {'user_id': user_id, 'name': name, 'username': username, 'password': password,
                              'email': email, 'status': 'success', 'message': 'User is created'}

    for key, value in expected_response_data.items():
        assert expected_response_data[key] == response.json()[key]
        # assert response.json() == expected_response_data

def test_post_request_to_create_existing_user():
    post_data_to_create_user = {'user_id': user_id, 'name': name, 'username': username, 'password': password, 'email': email}

    try:
        response = requests.post(f"{BASE_URL}/create_users", json=post_data_to_create_user)
        assert response.status_code == 200
    except Exception as err:
        print(err)
        assert False, f"POST request is failing due exception with message : {err}"

    expected_response_data = {'user_id': user_id, 'name': name, 'username': username, 'password': password,
                              'email': email, 'status': 'error', 'message': 'Requested user_id is already exist'}

    for key, value in expected_response_data.items():
        assert expected_response_data[key] == response.json()[key]

def test_get_existing_user():
    get_existing_user = {'user_id': user_id}

    try:
        response = requests.get(f"{BASE_URL}/users/{get_existing_user['user_id']}")
        assert response.status_code == 200
    except Exception as err:
        print(err)
        assert False, f"GET request is failing due exception with message : {err}"

    # print(response.json())

    expected_response_data =  {'user_id': user_id, 'name': name, 'username': username,
                               'email': email, 'status': 'success', 'message': 'User data is fetched without any issue'}

    for key, value in expected_response_data.items():
        assert expected_response_data[key] == response.json()[key]
    # assert response.json() == expected_response_data

def test_get_non_existing_user():
    get_existing_user = {'user_id': f"{user_id}test"}

    try:
        response = requests.get(f"{BASE_URL}/users/{get_existing_user['user_id']}")
    except Exception as err:
        print(err)
        assert False, f"GET request is failing due exception with message : {err}"
        assert response.status_code == 404

    # print(response.json())

    expected_response_data =  {"detail": "User not found"}

    assert response.json() == expected_response_data

def test_put_update_exist_user():

    put_data = {"user_id": user_id, "name": update_name, "email" : update_email}
    expected_put_data = {'name': update_name, 'email':  update_email, 'user_id': user_id,
                         'status': 'success', 'message': 'User data is updated without any issue'}

    response = requests.put(f"{BASE_URL}/users/{put_data['user_id']}", json=put_data)

    assert response.status_code == 200
    assert response.json() == expected_put_data

def test_put_update_non_existing_user():

    put_data = {"user_id": f"{user_id}test", "name": update_name, "email" : update_email}
    expected_put_data = {'name': update_name, 'email':  update_email, 'user_id': f'{user_id}test',
                         'status': 'error', 'message': 'User not Found'}

    response = requests.put(f"{BASE_URL}/users/{put_data['user_id']}", json=put_data)

    assert response.status_code == 200
    assert response.json() == expected_put_data

def test_delete_exist_user():

    delete_data = {'user_id': user_id, 'name': update_name, 'email' : update_email}
    expected_delete_data = {'user_id': user_id, 'status': 'success', 'message': 'User deleted successfully'}

    response = requests.delete(f"{BASE_URL}/users/{delete_data['user_id']}")

    assert response.status_code == 200
    assert response.json() == expected_delete_data

def test_delete_non_exist_user():

    delete_data = {'user_id': f'{user_id}test', 'name': update_name, 'email' : update_email}
    expected_delete_data = {'user_id':  f'{user_id}test', 'status': 'error', 'message': 'User not found'}

    response = requests.delete(f"{BASE_URL}/users/{delete_data['user_id']}")

    assert response.status_code == 200
    assert response.json() == expected_delete_data
