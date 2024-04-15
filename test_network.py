import re
from time import sleep

from playwright.sync_api import Page, Route

url = "https://gymlog.ru/profile/login/"


def test_request(page: Page):
    """Проверка валидации бэкенда после подмены данных в фронте"""

    def change_request(route: Route):
        """Подмена данных во фронтовой"""
        data = route.request.post_data
        print(data)
        if data:
            data = data.replace("User415", "pudinglor")

        route.continue_(post_data=data)

    page.route(re.compile('profile/authenticate/'), change_request)  # ловим запрос
    page.goto(url)
    page.locator('#email').fill("User415")
    page.locator('#password').fill("hTKiNu")
    page.get_by_role("button", name='Войти').click()
    # pytest test_network.py::test_request -s -v --headed --browser firefox


def test_response(page: Page):
    """Подмена данных в ответе сервера"""
    def change_response(route: Route):
        """Подмена данных ответа от сервера"""
        response = route.fetch()
        data = response.text()
        data = data.replace("User415", "Ebobo")
        route.fulfill(response=response, body=data)

    page.route(re.compile('profile/415/'), change_response)  # ловим запрос
    page.goto(url)
    page.locator('#email').fill("User415")
    page.locator('#password').fill("hTKiNu")
    page.get_by_role("button", name='Войти').click()
    page.get_by_role("link", name='Мой профиль').click()
    sleep(5)
    # pytest test_network.py::test_response -s -v --headed --browser firefox


# pip3 install pytest-playwright
# playwright install
# pytest -s -v --headed --browser firefox
