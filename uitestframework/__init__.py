"""
3/31/2019 Joshua Cruz
joshua.cruz15@upr.edu
Package for automatic ui testing using selenium webdriver
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.opera.options import Options as OperaOptions
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from uitestframework.pom import PageObjectModel

name = "uitestframework"


class UIListener(AbstractEventListener):
    """
    Event Listener for driver: Enables communication between the test case and Page Object Model
    """
    def __init__(self, pom_instance):
        self.pom = pom_instance

    def before_navigate_to(self, url, driver):
        self.pom.set_active_page(url, driver)


class UITestCaseMixin:
    """
    This class can be inherited by any TestCase Class with a defined driver_path and pom attributes

    driver_path: refers to the path to the Chrome driver with the
    """
    def setUp(self):
        self.assertTrue(hasattr(self, 'driver_path'),
                        'driver_path attribute must bet set for all classes inheriting from UITestCaseMixin.'
                        ' Drivers can be downloaded at https://www.seleniumhq.org/download/')
        self.assertTrue(hasattr(self, 'pom'), 'pom attribute must be set for all '
                                              'classes inheriting from UITestCaseMixin')
        self.assertTrue(isinstance(self.pom, PageObjectModel), 'pom attribute must an instance of PageObjectModel')

        # Instantiates driver using selected browser. Defaults to chrome
        options = self.get_options()
        if hasattr(self, 'browser') and not self.browser == 'chrome':
            if self.browser == 'firefox':
                self.driver = webdriver.Firefox(executable_path=self.driver_path, firefox_options=options)
            elif self.browser == 'opera':
                self.driver = webdriver.Opera(executable_path=self.driver_path, options=options)
        else:
            self.driver = webdriver.Chrome(executable_path=self.driver_path, chrome_options=options)
        self.driver = EventFiringWebDriver(self.driver, UIListener(self.pom))

    def get_options(self):
        """
        Used to provide options for selenium drivers
        :return: Option object for particular browser
        """
        options_dict = {
            'chrome': ChromeOptions,
            'firefox': FirefoxOptions,
            'opera': OperaOptions,
        }
        key = self.browser if hasattr(self, 'browser') else 'chrome'
        options = options_dict[key]()
        if hasattr(self, 'options'):
            for opt in self.options:
                options.add_argument(opt)
        return options


__version__ = '0.0.2'

