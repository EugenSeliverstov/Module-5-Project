import pytest
import requests

# Тестовый сценарий №1 (Поиск ближайшего заведения к конкретной локации)
@pytest.fixture
def geocode_base_url():
    return "https://geocode-maps.yandex.ru/1.x/?apikey=2fd5c994-1d9a-4c12-b654-bb859a04d497"
@pytest.fixture
def search_base_url():
    return "https://search-maps.yandex.ru/v1/?apikey=d2d043c5-7d71-4622-9990-00c815078189"
@pytest.fixture
def headers():
    return {}

# Шаг № 1: Поиск геолокации по адресу (например, г. Москва, ул. Б. Спасская, д. 27)
def test_geolocation_by_address(geocode_base_url, headers):
    url = f"{geocode_base_url}&geocode=москва большая спасская 27&format=json"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print(response.text)

# Шаг №2: Запрос топ-3 ближайших пивных баров
def test_top_3_bars(search_base_url, headers):
    url = f"{search_base_url}&text=пивной бар&lang=ru_RU&ll=37.642384,55.776365&spn=0.01,0.01&type=biz&results=3"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print(response.text)

#Шаг №3: Поиск ближайшего бара по URI (например,"ymapsbm1://org?oid=225375811717" + параметризация)
@pytest.mark.parametrize("uri, expected_bar_name", [
    ("ymapsbm1://org?oid=225375811717", "Гамбринус"),
    ("ymapsbm1://org?oid=1234567890", "Шварцкайзер"),
    ("ymapsbm1://org?oid=9876543210", "Золотая вобла"),
])
def test_specific_bar_by_uri(geocode_base_url, headers, uri, expected_bar_name):
    url = f"{geocode_base_url}&uri={uri}&format=json"
    response = requests.get(url, headers=headers)
    assert response.status_code ==200
    print(response.text)

# Проверка, что в ответе есть бар с нужным названием
    data = response.json()
    found = False
    for feature in data.get('response', {}).get('GeoObjectCollection', {}).get('featureMember', []):
        if expected_bar_name in feature.get('GeoObject', {}).get('name', ''):
            found = True
            break
    assert found, f"Бар с названием '{expected_bar_name}' не найден в ответе"
    print(f"Бар '{expected_bar_name}' найден в ответе.")


# Тестовый сценарий № 2 (Использование неверного api-ключа (для поиска по организациям))

@pytest.fixture
def geocode_base_wrong_url():
    return "https://geocode-maps.yandex.ru/1.x/?apikey=d2d043c5-7d71-4622-9990-00c815078189"

# Шаг № 1:Геолокация по адресу (например, г. Москва, ул. Б. Спасская, д. 27)
def test_geolocation_wrong(geocode_base_wrong_url, headers):
    url = f"{geocode_base_wrong_url}&geocode=Ярославский вокзал&format=json"
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    print(response.text)

# Тестовый сценарий №3 (Поиск фитнес-клуба в районе объекта в Москве)

@pytest.fixture
def base_url_go():
    return "https://geocode-maps.yandex.ru/1.x/?apikey=2fd5c994-1d9a-4c12-b654-bb859a04d497"
@pytest.fixture
def search_url_go():
    return "https://search-maps.yandex.ru/v1/?apikey=d2d043c5-7d71-4622-9990-00c815078189"

@pytest.fixture
def headers_go():
    return {}

# Шаг № 1: Поиск геолокации по объекту, с параметризацией (г. Москва, Ярославский вокзал)
@pytest.mark.parametrize("object_name, expected_status_code", [
    ("Ярославский вокзал, Москва", 200),
    ("Казанский вокзал, Москва", 400),
    ("Ленинградский вокзал, Москва", 400),
])
def test_geolocation_by_object(geocode_base_url, headers, object_name, expected_status_code):
    url = f"{geocode_base_url}&geocode=Ярославский вокзал&format=json"
    response = requests.get(url, headers=headers)
    assert response.status_code == expected_status_code
    print(f"Тест для объекта: {object_name}")

# Шаг №2: Запрос на поиск фитнес-клубов поблизости
def test_gym_names(search_base_url, headers):
     url = f"{search_base_url}&text=фитнес клуб&lang=ru_RU&ll=37.657332, 55.776684&spn=0.01,0.01&type=biz&results=3"
     response = requests.get(url, headers=headers)
     assert response.status_code == 200
     print(response.text)















