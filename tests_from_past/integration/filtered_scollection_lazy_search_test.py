# MIT License
#
# Copyright (c) 2015-2019 Iakiv Kramarenko
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from selene.api.past import config
from selene.api.past import css_class
from selene.common.none_object import NoneObject
from selene.api.past import SeleneDriver
from tests_from_past.past.acceptance import get_test_driver
from tests_from_past.integration.helpers import GivenPage

__author__ = 'yashaka'

driver = NoneObject('driver')  # type: SeleneDriver
GIVEN_PAGE = NoneObject('GivenPage')  # type: GivenPage
WHEN = GIVEN_PAGE  # type: GivenPage
original_timeout = config.timeout


def setup_module(m):
    global driver
    driver = SeleneDriver.wrap(get_test_driver())
    global GIVEN_PAGE
    GIVEN_PAGE = GivenPage(driver)
    global WHEN
    WHEN = GIVEN_PAGE


def teardown_module(m):
    driver.quit()


def setup_function(fn):
    global original_timeout
    config.timeout = original_timeout


def test_search_is_lazy_and_does_not_start_on_creation():
    GIVEN_PAGE.opened_empty()
    non_existent_collection = driver.all('.not-existing').filtered_by(css_class('special'))
    assert str(non_existent_collection)


def test_search_is_postponed_until_actual_action_like_questioning_count():
    GIVEN_PAGE.opened_empty()
    elements = driver.all('li').filtered_by(css_class('will-appear'))

    WHEN.load_body('''
                   <ul>Hello to:
                       <li>Anonymous</li>
                       <li class='will-appear'>Bob</li>
                       <li class='will-appear'>Kate</li>
                   </ul>''')
    assert len(elements) == 2


def test_search_is_updated_on_next_actual_action_like_questioning_count():
    GIVEN_PAGE.opened_empty()
    elements = driver.all('li').filtered_by(css_class('will-appear'))

    WHEN.load_body('''
                   <ul>Hello to:
                       <li>Anonymous</li>
                       <li class='will-appear'>Bob</li>
                       <li class='will-appear'>Kate</li>
                   </ul>''')
    assert len(elements) == 2

    WHEN.load_body('''
                   <ul>Hello to:
                       <li>Anonymous</li>
                       <li class='will-appear'>Bob</li>
                       <li class='will-appear'>Kate</li>
                       <li class='will-appear'>Joe</li>
                   </ul>''')
    assert len(elements) == 3