from pages import baseconfigbindingpage
from selenium.webdriver.remote.webdriver import WebDriver


class homepage(baseconfigbindingpage):
    def __init__(self, driver: WebDriver, base_url: str = 'http://www.baidu.com'):
        super().__init__(driver, base_url)
    
    def refresh_hot(self):
        with self.action_chains() as chains:
            chains.click(self.find_element_by_selector(self.config['selector']['hotsearch']))