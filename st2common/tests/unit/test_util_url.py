# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import unittest2

from st2common.util.url import get_url_without_trailing_slash
from six.moves import zip


class URLUtilsTestCase(unittest2.TestCase):
    def test_get_url_without_trailing_slash(self):
        values = [
            'http://localhost:1818/foo/bar/',
            'http://localhost:1818/foo/bar',
            'http://localhost:1818/',
            'http://localhost:1818',
        ]
        expected = [
            'http://localhost:1818/foo/bar',
            'http://localhost:1818/foo/bar',
            'http://localhost:1818',
            'http://localhost:1818',
        ]

        for value, expected_result in zip(values, expected):
            actual = get_url_without_trailing_slash(value=value)
            self.assertEqual(actual, expected_result)
