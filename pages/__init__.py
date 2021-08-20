from contextlib import contextmanager
from typing import ContextManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from functools import wraps
import json
from importlib import import_module
# from selenium.webdriver.support import expected_conditions as EC

def _need_init(func):
    @wraps(func)
    def decorator(self, *args, **kwargs):
        if not self.initialized():
            raise Exception('Page not initialized')
        return func(self, *args, **kwargs)
    return decorator

class basepage:


    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self._initialized = False

    def init(self, wait_condition=None, wait_timeout=10):
        self.driver.get(self.base_url)
        if wait_condition:
            wait = WebDriverWait(self.driver, wait_timeout)
            wait.until(wait_condition)
        self._initialized = True

    def initialized(self):
        return self._initialized

    @_need_init
    def find_element_by_selector(self, selector: str) -> WebElement:
        return self.driver.find_element_by_css_selector(selector)
    
    @_need_init
    def set_innerText(self, selector: str, innerText: str) -> WebElement:
        self.driver.execute_script(f'document.querySelector("{selector}").innerText="{innerText}"')
        return self.find_element_by_selector(selector)
    
    @_need_init
    def input_text(self, selector: str, text: str) -> WebElement:
        elem = self.find_element_by_selector(selector)
        elem.send_keys(text)
        return elem
    
    @_need_init
    def submit(self, selector) -> WebElement:
        elem = self.find_element_by_selector(selector)
        elem.submit()
        return elem

    @contextmanager
    def action_chains(self):
        try:
            action: ActionChains = ActionChains(self.driver)
            yield action
        finally:
            action.perform()
            action = None
        
class baseconfigbindingpage(basepage):
    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url)
        module = import_module(self.__module__)
        config_path = module.__file__.rsplit('.', 1)[0] + '.json'
        with open(config_path) as file:
            config = json.loads(file.read())
            self._config = config

    @property
    def config(self):
        return self._config