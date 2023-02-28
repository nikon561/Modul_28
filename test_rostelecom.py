from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import time
import consts


def get_driver():

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en-GB'})
    driver = webdriver.Chrome(executable_path=consts.driverPathChrome, chrome_options=options)

    driver.get(consts.baseUrl)
    driver.maximize_window()
    wait = WebDriverWait(driver, 30)
    assert wait.until(EC.presence_of_element_located((By.XPATH, '//h1[@class="card-container__title"]'))).text == 'Авторизация'
    return driver, wait


# TC-tD-001 Переход по ссылке "Зарегистрироваться"
def test_correct_redirect_to_register():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    time.sleep(5)
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'
    driver.quit()


# TC-tD-002 Регистрация по номеру телефона
def test_registration_phoneNumber():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
    actionChain.send_keys('Кириллица').perform()
    wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
    actionChain.send_keys('Кириллица').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    actionChain.send_keys('+79610535638').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
    actionChain.send_keys('Latinica2').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
    actionChain.send_keys('Latinica2').perform()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div > div > div:nth-of-type(2) > svg'))).click()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div:nth-of-type(2) > div > div:nth-of-type(2) > svg > path'))).click()
    time.sleep(5)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    confirmPage = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Подтверждение телефона')]"))).text
    assert confirmPage == 'Подтверждение телефона'
    driver.quit()


# TC-tD-003 Регистрация по e-mail
def test_registration_email():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
    actionChain.send_keys('КириллицаА').perform()
    wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
    actionChain.send_keys('КириллицаБ').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    actionChain.send_keys('nikon-va@yandex.ru').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
    actionChain.send_keys('Latinica2').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
    actionChain.send_keys('Latinica2').perform()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div > div > div:nth-of-type(2) > svg'))).click()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div:nth-of-type(2) > div > div:nth-of-type(2) > svg > path'))).click()
    time.sleep(5)
    driver.find_element(By.NAME, 'register').click()
    time.sleep(3)

    confirmPage = wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Подтверждение email')]"))).text
    assert confirmPage == 'Подтверждение email'
    driver.quit()


# TC-tD-004 Ввод данных в поля Имя и Фамилия на странице Регистрации
def test_register_firstName_and_lastName():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    firstNameInput = wait.until(EC.presence_of_element_located((By.NAME, 'firstName')))
    lastNameInput = wait.until(EC.presence_of_element_located((By.NAME, 'lastName')))


    elementsDictionary = {
        'firstName': firstNameInput,
        'lastName': lastNameInput
    }

    for key in consts.registerKeysDict:
        values = consts.registerKeysDict[key]

        actionChain.click(elementsDictionary[key]).perform()

        for j in range(len(values)):
            actionChain.send_keys(values[j]).perform()
            driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]").click()

            if j < len(values) - 1:
                if j >= 1:
                    pass
                else:
                    error = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text
                time.sleep(1)
                assert error == consts.registerErrorsName
                actionChain.double_click(elementsDictionary[key]).click_and_hold().send_keys(Keys.DELETE).perform()
    driver.quit()


# TC-tD-005 Ввод данных в поле "Email или Мобильный телефон" на странице Регистрации
def test_register_email_and_phone():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    addressNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address')))

    values = consts.registerFormKeysAddress
    actionChain.click(addressNameInput).perform()

    for j in range(len(values)):
        actionChain.send_keys(values[j]).perform()
        driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]").click()

        if j < len(values) - 1:
            if j >= 1:
                pass
            else:
                error = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text
            time.sleep(1)
            assert error == consts.registerErrorsAddress
            actionChain.double_click(addressNameInput).click_and_hold().send_keys(Keys.DELETE).perform()
    driver.quit()


# TC-tD-006 Ввод данных в поле Пароль на странице Регистрации
def test_register_password():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    passNameInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password')))
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                               'section#page-right > div > div > div > form > div:nth-of-type(4) > div > div > div:nth-of-type(2) > svg'))).click()

    values = consts.registerFormPassword
    actionChain.click(passNameInput).perform()

    for j in range(len(values)):
        actionChain.send_keys(values[j]).perform()
        driver.find_element(By.XPATH, "//p[contains(text(),'Личные данные')]").click()

        if j < len(values) - 1:
            if j >= 1:
                pass
            else:
                error = wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'span.rt-input-container__meta.rt-input-container__meta--error'))).text

            time.sleep(1)
            actionChain.double_click(passNameInput).click_and_hold().send_keys(Keys.DELETE).perform()
            assert error == consts.regErPass
    driver.quit()


# TC-tD-007 Проверка поля "Проверка Пароля" на странице Регистрации
def test_register_passwordConfirm():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.ID, 'kc-register'))).click()
    assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-container__title'))).text == 'Регистрация'

    wait.until(EC.presence_of_element_located((By.NAME, 'firstName'))).click()
    actionChain.send_keys('КирилицаА').perform()
    wait.until(EC.presence_of_element_located((By.NAME, 'lastName'))).click()
    actionChain.send_keys('КирилицаБ').perform()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#address'))).click()
    actionChain.send_keys('+79610535638').perform()
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div > div > div:nth-of-type(2) > svg'))).click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password'))).click()
    actionChain.send_keys('Latinica1').perform()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section#page-right > div > div > div > form > div:nth-of-type(4) > div:nth-of-type(2) > div > div:nth-of-type(2) > svg > path'))).click()
    time.sleep(1)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input#password-confirm'))).click()
    actionChain.send_keys('Latinica2').perform()
    time.sleep(1)
    driver.find_element(By.NAME, 'register').click()

    error = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Пароли не совпадают')]"))).text
    assert error == 'Пароли не совпадают'
    driver.quit()


# TC-tD-008  Переход по ссылке "Забыл пароль"
def test_click_forgotPassword():
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()

    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'
    driver.quit()


# TC-tD-009 Обновление капчи на странице Восстановления пароля
def test_refresh_captcha():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'

    oldCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')
    actionChain.move_to_element(driver.find_element(By.CLASS_NAME, 'rt-captcha__reload')).click().perform()

    driver.implicitly_wait(20)

    newCaptcha = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-captcha__image'))).get_attribute('src')
    assert oldCaptcha != newCaptcha
    driver.quit()


# TC-tD-010 Смена текста подсказки плейсхолдера в поле "Логин" при изменении способа авторизации.
def test_form_change():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'
    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))

    assert wait.until(EC.title_is('Ростелеком ID'))
    assert len(tabButtons) == 4

    for i in range(len(tabButtons)):
        actionChain.move_to_element(tabButtons[i]).click().perform()
        placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
        assert wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'rt-tab--active'))).text == driver.find_element(By.ID, consts.tabButtonsId[i]).text
        assert placeholderInput == consts.placeholderInputsValue[i]
    driver.quit()


# TC-tD-011 Кликабельность и работоспособность кнопки Вернуться назад, на странице Восстановление пароля.
def test_back_to_login():
    driver, wait = get_driver()

    wait.until(EC.presence_of_element_located((By.XPATH, "//a[@id='forgot_password']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Восстановление пароля')]"))).text == 'Восстановление пароля'

    wait.until(EC.presence_of_element_located((By.XPATH, "//button[@id='reset-back']"))).click()
    assert wait.until(EC.presence_of_element_located((By.XPATH, "//h1[contains(text(),'Авторизация')]"))).text == 'Авторизация'
    driver.quit()


# TC-tD-012 Автоматическая смена таба при вводе - телефона/почты/лицевого счета/логина на странице Авторизации.
def test_correct_change_input():
    driver, wait = get_driver()
    actionChain = ActionChains(driver)

    tabButtons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'rt-tab')))
    placeholderInput = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.rt-input__placeholder'))).text
    assert placeholderInput == consts.placeValue[0]

    for i in range(len(tabButtons)):
        actionChain.move_to_element(driver.find_element(By.ID, 'username')).click().perform()
        actionChain.send_keys(consts.sendedKeys[i]).perform()
        actionChain.move_to_element(driver.find_element(By.ID, 'password')).click().perform()
        activeTabButton = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, f'.rt-tabs .{consts.activeTab}')))
        assert activeTabButton.text == consts.tabTitlesAuth[i], driver.quit()
        time.sleep(2)
        actionChain.double_click(driver.find_element(By.ID, 'username')).click_and_hold().send_keys(Keys.DELETE).perform()

    driver.quit()


# TC-tD-013 Переход по ссылке в чат Телеграм.
def test_tg_chat():
    driver, wait = get_driver()
    actionChains = ActionChains(driver)
    chatTg = wait.until(EC.presence_of_element_located((By.ID, "widget_bar")))
    originalWindow = driver.current_window_handle
    actionChains.move_to_element(chatTg).perform()
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="alt-channel omnichat-theme-white svelte-1sezl8s"][2]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break

    assert driver.current_url.__contains__('https://telegram.me/Rostelecom_ChatBot')
    driver.quit()


# TC-tD-014 Переход по ссылке в чат Viber.
def test_viber_chat():
    driver, wait = get_driver()
    actionChains = ActionChains(driver)
    chatVb = wait.until(EC.presence_of_element_located((By.ID, "widget_bar")))
    originalWindow = driver.current_window_handle
    actionChains.move_to_element(chatVb).perform()
    wait.until(EC.presence_of_element_located((By.XPATH, '//a[@class="alt-channel omnichat-theme-white svelte-1sezl8s"][1]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    assert driver.current_url.__contains__('https://chats.viber.com/Rostelecom')

    driver.quit()


# TC-tD-015 Кликабельность и работоспособность ссылок Пользовательского соглашения и Политики конфиденциальности.
def test_open_agreement():
    driver, wait = get_driver()
    originalWindow = driver.current_window_handle

    wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'пользовательского соглашения'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    window_title = driver.execute_script("return window.document.title")
    time.sleep(3)
    assert window_title == 'User agreement'

    driver.close()

    driver.switch_to.window(originalWindow)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[1]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    window_title = driver.execute_script("return window.document.title")
    time.sleep(3)
    assert window_title == 'User agreement'

    driver.close()

    driver.switch_to.window(originalWindow)
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="rt-footer-agreement-link"]/span[2]'))).click()
    WebDriverWait(driver, 5).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != originalWindow:
            driver.switch_to.window(window_handle)
            break
    window_title = driver.execute_script("return window.document.title")
    time.sleep(3)
    assert window_title == 'User agreement'

    driver.quit()


# TC-tD-016 Переход по ссылке авторизации пользователя с помощью VK.
def test_try_auth_with_vk():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_vk'))).click()
    time.sleep(2)

    assert driver.current_url.__contains__('oauth.vk.com')
    driver.quit()

# TC-tD-017 Переход по ссылке авторизации пользователя с помощью OК.
def test_try_auth_with_ok():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ok'))).click()
    time.sleep(2)

    assert driver.current_url.__contains__('connect.ok.ru')
    driver.quit()

# TC-tD-018 Переход по ссылке авторизации пользователя с помощью Mail.ru.
def test_try_auth_with_mail():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_mail'))).click()
    time.sleep(2)

    assert driver.current_url.__contains__('connect.mail.ru')
    driver.quit()

# TC-tD-019 Переход по ссылке авторизации пользователя с помощью Google.
def test_try_auth_with_google():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_google'))).click()
    time.sleep(2)

    assert driver.current_url.__contains__('accounts.google.com')
    driver.quit()

# TC-tD-020 Переход по ссылке авторизации пользователя с помощью Yandex.
def test_try_auth_with_yandex():
    driver, wait = get_driver()
    wait.until(EC.presence_of_element_located((By.ID, 'oidc_ya'))).click()
    time.sleep(2)

    assert driver.current_url.__contains__('oauth.yandex.ru')
    driver.quit()