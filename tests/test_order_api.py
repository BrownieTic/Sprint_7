import allure
import json
import pytest

from data import OrderParametrs as parametrs
from api.order_api import OrderAPI

@allure.feature("Заказы")
class TestOrderAPI:
    request = OrderAPI()
    @allure.story("Создание заказа")
    @allure.title("Создание заказа самоката с цветом: {color}")
    @pytest.mark.parametrize('color',
        [['GREY', 'BLACK'], 
        ['BLACK'],
        [],
        None]
        )
    def test_create_order_api_all_fields_success(self, color, user_data_copy):
        user_data_copy["color"] = color
        with allure.step("Создать заказ"):
            response = self.request.create_order_request(user_data_copy)

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 201
            assert 'track' in response.json()

@allure.feature("Получение списка заказов")
class TestOrderListAPI:
    request = OrderAPI()

    @allure.story("Получение списка заказов с параметрами и проверка общего вида ответа")
    @allure.title("Получение списка заказов: параметр {parametr}")
    @pytest.mark.parametrize('parametr',
        ['', 
        'nearestStation=4',
        'limit=1',
        'page=0',
        'courierId=811393',
        'courierId=811393&nearestStation=4&limit=1&page=0'
        ]
        )
    def test_get_list_order_one_parametr_code_200_and_correct_format(self, parametr):
        with allure.step(f"Отправить GET-запрос с параметром: {parametr or 'без параметров'}"):
            response = self.request.get_list_order_request(parametr)
        with allure.step("Проверить статус-код ответа и основные поля"):
            assert response.status_code == 200
            assert 'orders' in response.json()
            assert 'pageInfo' in response.json()
        with allure.step("Проверить формат pageInfo"):
            page_info = response.json()['pageInfo']
            for field, expected_type in parametrs.PAGE_INFO_FIELDS.items():
                assert field in page_info
                assert isinstance(page_info[field], expected_type)

    @allure.story("Получение списка заказов и проверка значений параметров")
    @allure.title("Фильтрация заказов по courierId и nearestStation")
    def test_get_list_order_parametrs_courierId_and_nearestStation_correct_values(self, register_courier_and_order):
        test_data = register_courier_and_order
        metro_station = str(test_data["order_data"]["metroStation"])
        params = {
                "courierId": test_data["courier_id"],
                "nearestStation": json.dumps([metro_station])
        }
        with allure.step("Получить список заказов по courierId и nearestStation"):
            response = self.request.get_list_order_request(params)
        with allure.step("Проверить код ответа и данные заказа"):
            order = response.json()['orders'][0]
            assert response.status_code == 200
            assert order['courierId'] == test_data["courier_id"]
            assert order['metroStation'] == metro_station

    @allure.title("Проверка limit и page с courierId")
    @pytest.mark.parametrize('string, param',
        [("limit", parametrs.limit), 
        ("page",parametrs.page)
        ]
        )
    def test_get_list_order_parametrs_courierId_and_page_info_correct_values(self, register_courier_and_order, string, param):
        test_data = register_courier_and_order
        params = {
                "courierId": test_data["courier_id"],
                string: param
        }
        with allure.step(f"Получить список заказов с courierId и {string}={param}"):
            response = self.request.get_list_order_request(params)
        with allure.step("Проверить код ответа, courierId и параметр из pageInfo"):
            assert response.status_code == 200
            order = response.json()['orders'][0]
            page_info = response.json()["pageInfo"]
            assert order['courierId'] == test_data["courier_id"]
            assert page_info[string] == param

    @allure.title("Проверка limit и page с nearestStation")
    @pytest.mark.parametrize('string, param',
        [("limit", parametrs.limit), 
        ("page",parametrs.page)
        ]
        )
    def test_get_list_order_parametrs_nearestStation_and_page_info_correct_values(self, register_courier_and_order, string, param):
        test_data = register_courier_and_order
        metro_station = str(test_data["order_data"]["metroStation"])
        params = {
                "nearestStation": json.dumps([metro_station]),
                string : param
        }
        with allure.step(f"Получить список заказов с nearestStation и {string}={param}"):
            response = self.request.get_list_order_request(params)
        with allure.step("Проверить код ответа,nearestStation и параметр из pageInfo"):
            assert response.status_code == 200
            order = response.json()['orders'][0]
            page_info = response.json()["pageInfo"]
            assert order['metroStation'] == metro_station
            assert page_info[string] == param

    @allure.title("Проверка одновременной фильтрации limit и page")
    def test_get_list_order_parametrs_limit_and_page_correct_values(self, register_courier_and_order):
        params = {
                "limit": parametrs.limit,
                "page": parametrs.page
        }
        with allure.step("Получить список заказов с limit и page"):
            response = self.request.get_list_order_request(params)
        with allure.step("Проверить код ответа и значения pageInfo"):
            assert response.status_code == 200
            page_info = response.json()["pageInfo"]
            assert page_info['limit'] == parametrs.limit
            assert page_info['page'] == parametrs.page
