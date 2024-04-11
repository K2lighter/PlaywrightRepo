import re
from playwright.sync_api import Page, Route

url = "https://gymlog.ru/profile/login/"


def test_request(page: Page):
    """Проверка валидации бэкенда после подмены данных в фронте"""
    def change_request(route: Route):
        """Подмена данных фронтовой валидации"""
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

# pip3 install pytest-playwright
# playwright install
# pytest -s -v --headed --browser firefox
