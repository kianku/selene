import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selene import Config, Browser


@pytest.fixture(scope='session')
def session_driver():
    chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture(scope='function')
def session_browser(session_driver, request):
    try:
        timeout = request.param
    except AttributeError:
        timeout = Config().timeout
        print(timeout)
    yield Browser(Config(driver=session_driver, timeout=timeout))