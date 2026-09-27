
class UserData:
    USER = {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
    }

class OrderParametrs:
    nearestStation = 4
    limit = 1
    page = 0

    PAGE_INFO_FIELDS = {
        'page': int,
        'total': int,
        'limit': int,
    }
