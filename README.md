
UI Test Framework
===========
Package for Testing Browser User interfaces.

Installation
===========
      pip install uitestframework

Usage
===========
The UI Test Framework provides a base for creating browser based UI tests by using the Page Object Model and selenium
 webdriver. You might find
it most useful for testing web application in development in which the UI is continually being changed. Typical usage
often looks like this::

    #!/usr/bin/env python

    from unittest import TestCase

    from uitestframework import UITestCaseMixin, PageObjectModel
    from uitestframework.pom import BasePage, BaseElement

    APPLICATION_HOST = "https://localhost:8080"


    class MyPage(BasePage):
        def set_elements(self):
            # adds a BaseElement instance "Button1" to MyPage
            button1 = BaseElement(name="Button1", locator="button_id", locator_type='id', page=self)
            return [button1]


    class MyPOM(PageObjectModel):
        # Maps url paths to BasePage instance
        url_map = {
            '': MyPage,
        }


    class MyTestCase(UITestCaseMixin, TestCase):
        # These are necessary attributes for this class
        driver_path = "chromedriver.exe"
        browser = 'chrome'
        pom = MyPOM()

        def test_foo(self):
            # tests that button 1 redirects you from the current page
            self.driver.get(APPLICATION_HOST)
            # Using the url map, the pom knows in which page to look for the specified element attribute
            # Several methods for interacting with UI are implemented in the BaseElement class and its Subclasses
            self.pom.button1.click()
            self.assertTrue(self.driver.current_url != APPLICATION_HOST)

To test pages which require user input. The FormPage class can be used. An example of usage is provided below::

    #!/usr/bin/env python

    from unittest import TestCase

    from uitestframework import UITestCaseMixin, PageObjectModel
    from uitestframework.pom import BasePage, BaseElement

    APPLICATION_HOST = "https://localhost:8080"


    class LoginPage(FormPage):

        def set_elements(self):
            username = FieldElement(name='username', locator="id_username", locator_type=By.ID, page=self)
            password = FieldElement(name='password', locator="id_password", locator_type=By.ID, page=self)
            submit = FieldElement(name='submit', locator="id_submit", locator_type=By.ID, page=self)
            error_message = BaseElement(name='error_message", locator="id_error", locator_type=By.ID, page=self)
            return [username, password, submit, error_message]


    class MyApplicationPOM(PageObjectModel):
        url_map = {
            /login: LoginPage,
        }


    class MyTestCase(UITestCaseMixin, TestCase):
        driver_path = "chromedriver.exe"
        browser = 'chrome'
        pom = MyApplicationPOM()

        def test_login(self):
            login_url = APPLICATION_HOST + '/login'
            self.driver.get(login_url)
            self.pom.autofill(username='username', password='correct password')
            self.pom.submit.click()
            self.assertTrue(self.driver.current_url != login_url)

        def test_failed_login(self):
            login_url = APPLICATION_HOST + '/login'
            self.driver.get(login_url)
            self.pom.autofill(username='username', password='wrong password')
            self.pom.submit.click()
            self.assertTrue(self.pom.error_message.is_rendered())