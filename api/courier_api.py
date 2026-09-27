import requests
import allure

from urls import API as api

class CourierAPI:
    def create_courier_request(self, data):
        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(api.creating_courier_api, data = data)
        return response

    def login_courier_request(self, data):
        with allure.step("Отправка запроса на авторизацию курьера"):
            response = requests.post(api.login_courier_api, data=data)
        return response

    def delet_courier_request(self, courier_id):
        response = requests.delete(f'{api.delete_courier_api}/{courier_id}')
        return response