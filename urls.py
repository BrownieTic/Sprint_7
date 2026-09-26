class Url:
    MAIN_PAGE_URL = 'https://qa-scooter.praktikum-services.ru/'

class API:
    creating_courier_api = f'{Url.MAIN_PAGE_URL}api/v1/courier'
    login_courier_api = f'{Url.MAIN_PAGE_URL}api/v1/courier/login'
    delete_courier_api = f'{Url.MAIN_PAGE_URL}/api/v1/courier'

    order_api = f'{Url.MAIN_PAGE_URL}api/v1/orders'