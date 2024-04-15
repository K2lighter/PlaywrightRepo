from time import sleep
from playwright.sync_api import Page, expect, Dialog


def test_alert_first(page: Page):
    """
    Зайти на страницу, кликнуть на ссылку, после перехода убедиться, что все текст совпадает с тз,
    добавляем товар, ждем появления Алерта, согласиться с алертом, перейти в корзину
    """
    page.goto('https://www.demoblaze.com/')

    def accept_alert(alert: Dialog):
        """
        функция для подтверждения алерта
        """
        print(alert.message)
        alert.accept()

    page.on('dialog', accept_alert)  # on - когда происходит диалог, вызови функцию

    page.get_by_role('link', name='Samsung galaxy s6').click()
    expect(page.get_by_text('PRODUCT STORE')).to_be_visible()  # убедиться, что на странице есть текст
    expect(page.locator('xpath=//h2[@class="name"]')).to_have_text("Samsung galaxy s6")  # чекаем текст по локатору
    page.locator('xpath=//a[@onclick="addToCart(1)"]').click()  # добавляем товар в корзину
    page.wait_for_event('dialog')  # ждем появления алерта
    page.locator('#cartur').click()
    sleep(3)
