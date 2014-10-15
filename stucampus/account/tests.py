# -*- coding: utf=8
from urlparse import urljoin

from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from selenium import webdriver

from stucampus.account.models import Student


class AccountTest(LiveServerTestCase):

    def setUp(self):
        super(AccountTest, self).setUp()
        user = User.objects.create_user(
            'test@test.com', 'test@test.com', 'password')
        self.student = Student.objects.create(user=user, screen_name='test')
        self.browser = webdriver.PhantomJS()

    def tearDown(self):
        self.browser.close()

    def find_id(self, _id):
        return self.browser.find_element_by_id(_id)

    def find_css(self, selector):
        browser = self.browser
        return browser.find_element_by_css_selector(selector)

    def get_msg_element_by_class(self, class_name):
        message_box = self.find_id('message-box')
        elems = message_box.find_elements_by_class_name(class_name)
        self.assertTrue(len(elems) > 0)
        return elems[0]

    def signup(self, email, password, confirm):
        self.browser.get(self.reverse_url('account:sign_up'))
        email_f = self.find_css('input[name=email]')
        passwd_f = self.find_css('input[name=password]')
        confirm_f = self.find_css('input[name=confirm]')
        signup_btn = self.find_css('input[type=submit]')
        email_f.send_keys(email)
        passwd_f.send_keys(password)
        confirm_f.send_keys(confirm)
        signup_btn.click()

    def signin(self, email, password):
        self.browser.get(self.reverse_url('account:sign_in'))
        email_f = self.find_css('input[name=email]')
        passwd_f = self.find_css('input[name=password]')
        signin_btn = self.find_css('input[type=submit]')
        email_f.send_keys(email)
        passwd_f.send_keys(password)
        signin_btn.click()

    def get_url(self, url):
        return urljoin(self.live_server_url, url)

    def reverse_url(self, viewname, urlconf=None, args=None, kwargs=None):
        url = reverse(viewname, urlconf, args, kwargs)
        return self.get_url(url)

    def test_signup_success(self):
        self.signup('test@gmail.com', 'input-password', 'input-password')
        msg = self.get_msg_element_by_class('notice')
        self.assertIn(u'注册成功', msg.text)

    def test_signup_no_email(self):
        self.signup('', 'input-password', 'input-password')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'Email', msg.text)
        self.assertIn(u'require', msg.text)

    def test_signup_no_password(self):
        self.signup('test@gmail.com', '', 'input-password')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'Password', msg.text)
        self.assertIn(u'require', msg.text)

    def test_signup_no_confirm(self):
        self.signup('test@gmail.com', 'input-password', '')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'Repeat password', msg.text)
        self.assertIn(u'require', msg.text)

    def test_signup_no_match(self):
        self.signup('test@gmail.com', 'input-password', 'other-password')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'Password', msg.text)
        self.assertIn(u'match', msg.text)

    def test_signup_exist(self):
        self.signup('test@test.com', 'input-password', 'input-password')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'Email', msg.text)
        self.assertIn(u'exist', msg.text)

    def test_signup_too_short(self):
        self.signup('test@gmail.com', 'short', 'short')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'Password', msg.text)
        self.assertIn(u'6', msg.text)
        self.assertIn(u'more character', msg.text)

    def test_signup_wrong_email_format(self):
        self.signup('test', 'input-password', 'input-password')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn(u'valid', msg.text)
        self.assertIn(u'email', msg.text)

    def test_signin_success(self):
        self.signin('test@test.com', 'password')
        msg = self.get_msg_element_by_class('notice')
        self.assertIn(u'登录成功', msg.text)

    def test_signin_no_email(self):
        self.signin('', 'password')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn('Email', msg.text)
        self.assertIn('require', msg.text)

    def test_signin_no_password(self):
        self.signin('test@test.com', '')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn('Password', msg.text)
        self.assertIn('require', msg.text)

    def test_signin_wrong(self):
        self.signin('test@test.com', '000123456')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn('email', msg.text)
        self.assertIn('password', msg.text)
        self.assertIn('incorrect', msg.text)

    def test_signin_too_short(self):
        self.signin('test@test.com', '000')
        msg = self.get_msg_element_by_class('alert')
        self.assertIn('Password', msg.text)
        self.assertIn(u'6', msg.text)
        self.assertIn(u'more character', msg.text)
