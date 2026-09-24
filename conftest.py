import pytest
import requests

from urls import API as api
from data import RandomData
from data import UserData as user_data


@pytest.fixture(scope="function")
def create_random_courier_data():
    data = RandomData()
    # генерируем логин, пароль и имя курьера
    login = data.generate_random_string(10)
    password = data.generate_random_string(10)
    first_name = data.generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return payload

@pytest.fixture(scope="function")
def register_courier_and_delete(create_random_courier_data):
    # отправляем запрос на регистрацию курьера
    requests.post(api.creating_courier_api, data=create_random_courier_data)

    payload = {
        "login": create_random_courier_data["login"],
        "password": create_random_courier_data["password"]
    }
    yield payload

    if "id" in payload:
        courier_id = payload["id"]
        requests.delete(f'{api.delete_courier_api}{courier_id}')

@pytest.fixture(scope="function")
def get_id_courier_and_delete(create_random_courier_data):
    yield create_random_courier_data
    payload = {
        "login": create_random_courier_data["login"],
        "password": create_random_courier_data["password"]
    }
    response = requests.post(api.id_courier_api, data=payload)
    courier_id = response.json()["id"]
    requests.delete(f'{api.delete_courier_api}{courier_id}')

@pytest.fixture(scope="function")
def user_data_copy():
    user_data_copy = user_data.USER.copy()
    return user_data_copy

@pytest.fixture(scope="function")
def register_courier_and_order(create_random_courier_data, user_data_copy):
    create_courier_response = requests.post(api.creating_courier_api, json=create_random_courier_data)
    assert create_courier_response.status_code == 201
    response_courier = requests.post(api.id_courier_api, json={
                "login": create_random_courier_data["login"],
                "password": create_random_courier_data["password"],
            })
    assert response_courier.status_code == 200

    # Получаем id курьера
    courier_id = response_courier.json()["id"]
    # Создаём заказ
    create_order_response = requests.post(api.order_api, json=user_data_copy)
    assert create_order_response.status_code == 201
    track = create_order_response.json()["track"]
    # Получаем заказ по track и узнаём его id
    get_order_response = requests.get(f'{api.order_api}/track', 
                                      params={"t": track})
    assert get_order_response.status_code == 200
    order = get_order_response.json()["order"]
    order_id = order["id"]
    # Принимаем заказ курьером
    requests.put(f'{api.order_api}/accept/{order_id}', 
                 params={"courierId": courier_id})
    yield {
            "courier_id": courier_id,
            "order_id": order_id,
            "order_data": user_data_copy,
        }

    requests.delete(f'{api.delete_courier_api}{courier_id}')
