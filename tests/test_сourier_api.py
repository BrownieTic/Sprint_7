import requests
import allure

from urls import API as api

@allure.feature("Курьеры")
class TestCourierAPI:
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера")
    def test_creat_courier_all_fields_success(self, get_id_courier_and_delete):
        with allure.step("Отправка запроса на создание курьера"):
            response = requests.post(api.creating_courier_api, data=get_id_courier_and_delete)
        with allure.step("Проверка успешного создания курьера"):
            assert response.status_code == 201
            assert response.json() == {"ok": True}

    @allure.story("Создание курьера")
    @allure.title("Создание курьера с уже занятым логином")
    def test_creat_twin_couriers_all_field_get_error(self, get_id_courier_and_delete):
        with allure.step("Отправка запросов на создание курьера"):
            response = requests.post(api.creating_courier_api, data=get_id_courier_and_delete)
            response = requests.post(api.creating_courier_api, data=get_id_courier_and_delete)
        with allure.step("Проверка ошибки занятого логина"):
            assert response.status_code == 409
            assert response.json() == {"message": "Этот логин уже используется"}

    @allure.story("Валидация создания курьера")
    @allure.title("Создание курьера без логина")
    def test_creat_courier_without_login_error(self, create_random_courier_data):
        with allure.step("Отправка запроса без логина"):
            response = requests.post(api.creating_courier_api, data={
                "password": create_random_courier_data["password"],
                "firstName": create_random_courier_data["firstName"]})
        with allure.step("Проверка ошибки отсутствия логина"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}

    @allure.story("Валидация создания курьера")
    @allure.title("Создание курьера без пароля")
    def test_creat_courier_without_password_error(self, create_random_courier_data):
        with allure.step("Отправка запроса без пароля"):
            response = requests.post(api.creating_courier_api, data={
                "login": create_random_courier_data["login"],
                "firstName": create_random_courier_data["firstName"]})
        with allure.step("Проверка ошибки отсутствия пароля"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для создания учетной записи"}

@allure.feature("Авторизация курьера")
class TestLoginCourierAPI:
    @allure.story("Успешная авторизация")
    @allure.title("Авторизация курьера с корректными данными")
    def test_login_courier_all_fields_success(self, register_courier_and_delete):
        with allure.step("Отправка запроса на авторизацию курьера"):
            response = requests.post(api.id_courier_api, data=register_courier_and_delete)
            response_json = response.json()["id"]
        with allure.step("Проверка успешной авторизации курьера"):
            assert response.status_code == 200
            assert "id" in response.json()

        register_courier_and_delete["id"] = response_json

    @allure.story("Валидация авторизации")
    @allure.title("Авторизация курьера без логина")
    def test_login_courier_without_login_error(self, register_courier_and_delete):
        with allure.step("Отправка запроса без логина"):
            response = requests.post(api.id_courier_api, data={"password": register_courier_and_delete["password"]})

        with allure.step("Проверка ошибки отсутствия логина"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для входа"}

    @allure.story("Валидация авторизации")
    @allure.title("Авторизация курьера без пароля")
    def test_login_courier_without_password_error(self, register_courier_and_delete):
        with allure.step("Отправка запроса без пароля"):
            response = requests.post(api.id_courier_api, data={"login": register_courier_and_delete["login"]})

        with allure.step("Проверка ошибки отсутствия пароля"):
            assert response.status_code == 400
            assert response.json() == {"message": "Недостаточно данных для входа"}

    @allure.story("Валидация авторизации")
    @allure.title("Авторизация с несуществующим логином")
    def test_login_courier_wrong_login_error(self, register_courier_and_delete):
        with allure.step("Отправка запроса с несуществующим логином"):
            response = requests.post(api.id_courier_api, data={
                "login": register_courier_and_delete["login"]*2, 
                "password": register_courier_and_delete["password"]
                })

        with allure.step("Проверка ошибки несуществующего логина"):
            assert response.status_code == 404
            assert response.json() == {"message": "Учетная запись не найдена"}

    @allure.story("Валидация авторизации")
    @allure.title("Авторизация с неверным паролем")
    def test_login_courier_wrong_password_error(self, register_courier_and_delete):
        with allure.step("Отправка запроса с неверным паролем"):
            response = requests.post(api.id_courier_api, data={
                "login": register_courier_and_delete["login"], 
                "password": register_courier_and_delete["password"]*2
                })

        with allure.step("Проверка ошибки неверного пароля"):
            assert response.status_code == 404
            assert response.json() == {"message": "Учетная запись не найдена"}

    @allure.story("Валидация авторизации")
    @allure.title("Авторизация с неверным логином и паролем")
    def test_login_courier_wrong_both_fields_error(self, register_courier_and_delete):
        with allure.step("Отправка запроса с неверным логином и паролем"):
            response = requests.post(api.id_courier_api, data={
                "login": register_courier_and_delete["login"]*2, 
                "password": register_courier_and_delete["password"]*2
                })

        with allure.step("Проверка ошибки неверных данных"):
            assert response.status_code == 404
            assert response.json() == {"message": "Учетная запись не найдена"}
        