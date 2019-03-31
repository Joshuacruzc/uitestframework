"""
3/31/2019 Joshua Cruz
joshua.cruz15@upr.edu
Package for automatic ui testing using selenium webdriver
"""
from selenium import webdriver
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
        if hasattr(self, 'browser') and not self.browser == 'chrome':
            if self.browser == 'firefox':
                self.driver = webdriver.Firefox(executable_path=self.driver_path)
            elif self.browser == 'opera':
                self.driver = webdriver.Opera(executable_path=self.driver_path)
            elif self.browser == 'internet_explorer':
                self.driver = webdriver.Ie(executable_path=self.driver_path)
            elif self.browser == 'safari':
                self.driver = webdriver.Safari(executable_path=self.driver_path)
        else:
            self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.driver = EventFiringWebDriver(self.driver, UIListener(self.pom))


__version__ = '0.0.0'

