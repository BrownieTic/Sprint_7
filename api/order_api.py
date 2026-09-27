import requests
import allure

from urls import API as api

class OrderAPI:
    def create_order_request(self, data):
        with allure.step("Создать заказ"):
            response = requests.post(api.order_api, json=data)
        return response

    def get_list_order_request(self, parametr):
        with allure.step(f"Отправить GET-запрос с параметром: {parametr or 'без параметров'}"):
            response = requests.get(api.order_api, params=parametr)
        return response
    
    def get_order_request(self, track):
        response = requests.get(f'{api.order_api}/track', 
                                      params={"t": track})
        return response

    def accept_order_request(self, order_id, courier_id):
        response = requests.put(f'{api.order_api}/accept/{order_id}', 
                         params={"courierId": courier_id})
        return response
    