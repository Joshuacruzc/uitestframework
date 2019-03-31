from urllib.parse import urlparse

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class PageObjectModel:
    """
    class to establish mapping between urls and BasePage
    """
    url_map = {}  # Keys should be url paths (excluding host and port). Values should point to a subclass of BasePage
    active_page = None

    def set_active_page(self, url, driver):
        """
        Will get BasePage mapped to given url and set it as active. The active page can be accessed via the POM instance
        pom.active_page.random element is the same as pom.random_element where pom is an instance of PageObjectModel
        :param url: The url to which the BasePage to be used is mapped.
        :param driver:
        :return: None
        """
        url_path = urlparse(url).path
        try:
            self.active_page = self.url_map[url_path](driver)
        except KeyError:
            print(f'No BasePage instance found in url_map for "{url_path}"')
            pass

    def __getattr__(self, item):
        return getattr(self.active_page, item)


class BasePage:
    """
    BasePage class corresponds to a specific page/url in the target application. It contains BaseElements
     belonging that page.
    """
    def __init__(self, driver):
        self.driver = driver
        for element in self.set_elements():
            setattr(self, element.name, element)

    def set_elements(self):
        """
        set_elements should return a list of the elements that will be assigned to the BasePage. They will be assigned
        as attributes when the class is initialized
        :return: list of BaseElements instances
        """
        raise NotImplementedError


class FormPage(BasePage):
    """
    FormPage should contain FieldElements that belong to a Form. Methods implemented in this class will be useful to
    test out user input through forms and different types of Fields.
    """
    def autofill(self, **kwargs):
        """
        Fills out a form using the values in kwargs as the user input, and the keys to these values as the name of the
        FieldElements to be filled
        :param kwargs: keys: FieldElement name, values: input to be written
        :return: None
        """
        for field in kwargs.keys():
            if hasattr(self, field):
                if isinstance(self.__getattribute__(field), FieldElement):
                    self.__getattribute__(field).write(kwargs[field], **kwargs)

    def set_elements(self):
        raise NotImplementedError


class BaseElement:
    """
    BaseElement class contains methods that can be used on any sort of HTML element.
    """
    def __init__(self, name, locator=None, locator_type=By.ID, page=None, **kwargs):
        """
        :param name: String: Name of the element, will be used to access it through the BasePage.
        :param locator: String: The value by which the Element will be found in the UI
        :param locator_type: String: The attribute to which the locator corresponds in the UI. I.e 'id'
        :param page: BasePage: The BasePage instance to which the element belongs.
=        """
        self.name = name
        self.locator = (locator_type, locator)
        self.driver = page.driver

    def find(self, **kwargs):
        """
        Uses the defined locator to find the UI element that corresponds to this BaseElement using selenium.
        :return:
        """
        try:
            return self.driver.find_element(*self.locator)
        except NoSuchElementException as e:
            raise Exception("Element with locator " + self.locator[1] + " not found in " + urlparse(
                self.driver.current_url).path) from e

    def click(self, **kwargs):
        """
        Clicks on the found UI element
        :return: None
        """
        el = self.find(**kwargs)
        el.click()


class FieldElement(BaseElement):
    """
    BaseElement that can receive user input.
    """
    def __init__(self, default=None, **kwargs):
        """
        Sets default attribute to Field Element. Said attribute will be used as input when no input is specified for
        this field.
        :param default: String: Default user input.
        """
        self.default = default
        super().__init__(**kwargs)

    def write(self, keys=None, **kwargs):
        """
        Writes keys as user input to the FieldElement
        :param keys: String: user input.
        :return: None
        """
        el = self.find(**kwargs)
        if el and el.is_enabled():
            if keys:
                el.send_keys(keys)
            else:
                el.send_keys(self.default)
