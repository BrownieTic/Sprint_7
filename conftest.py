import pytest

from randomizer import RandomData
from data import UserData as user_data
from api.courier_api import CourierAPI
from api.order_api import OrderAPI


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
    request_courier = CourierAPI()
    # отправляем запрос на регистрацию курьера
    request_courier.create_courier_request(create_random_courier_data)

    payload = {
        "login": create_random_courier_data["login"],
        "password": create_random_courier_data["password"]
    }
    yield payload

    if "id" in payload:
        courier_id = payload["id"]
        request_courier.delet_courier_request(courier_id)

@pytest.fixture(scope="function")
def get_id_courier_and_delete(create_random_courier_data):
    yield create_random_courier_data
    request_courier = CourierAPI()
    payload = {
        "login": create_random_courier_data["login"],
        "password": create_random_courier_data["password"]
    }
    response = request_courier.login_courier_request(payload)
    courier_id = response.json()["id"]
    request_courier.delet_courier_request(courier_id)

@pytest.fixture(scope="function")
def user_data_copy():
    user_data_copy = user_data.USER.copy()
    return user_data_copy

@pytest.fixture(scope="function")
def register_courier_and_order(create_random_courier_data, user_data_copy):
    request_order = OrderAPI()
    request_courier = CourierAPI()
    create_courier_response = request_courier.create_courier_request(create_random_courier_data)

    response_courier = request_courier.login_courier_request({
                "login": create_random_courier_data["login"],
                "password": create_random_courier_data["password"],
            })

    # Получаем id курьера
    courier_id = response_courier.json()["id"]
    # Создаём заказ
    create_order_response = request_order.create_order_request(user_data_copy)

    track = create_order_response.json()["track"]
    # Получаем заказ по track и узнаём его id
    get_order_response = request_order.get_order_request(track)
    
    order = get_order_response.json()["order"]
    order_id = order["id"]
    # Принимаем заказ курьером
    request_order.accept_order_request(order_id, courier_id)
    yield {
            "courier_id": courier_id,
            "order_id": order_id,
            "order_data": user_data_copy,
        }

    request_courier.delet_courier_request(courier_id)
