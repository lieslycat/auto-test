from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox import webdriver
from pages import basepage
from selenium import webdriver
import pytest
from pages.badiu.homepage import homepage

driver = None

def setup_module():
    global driver
    driver = webdriver.Firefox()

# def teardown_module():
#     global driver
#     driver.close()

# @pytest.mark.parametrize('query_str', ['pingping a dog', 'huihui a good guy'])
@pytest.mark.skip
def test_baidu(query_str):
    page = basepage(driver, 'https://www.baidu.com')
    page.init()
    page.input_text('#kw', query_str).submit()
    assert 'xiaohuihui is a dog' in driver.page_source

@pytest.mark.skip
def test_action(base_url):
    page = basepage(driver, base_url)
    page.init()
    with page.action_chains() as action:
        action.click(page.find_element_by_selector('#hotsearch-refresh-btn'))

def test_baidu_home():
    page = homepage(driver)
    page.init()
    page.refresh_hot()

@pytest.fixture()
def query_str():
    yield 'pingping a dog'
    return

@pytest.fixture()
def base_url():
    return 'http://www.baidu.com'