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
import os

__all__ = [
    'DEFAULT_LOGGING_CONF_PATH'
]

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DEFAULT_LOGGING_CONF_PATH = os.path.join(BASE_PATH, '../conf/base.logging.conf')
DEFAULT_LOGGING_CONF_PATH = os.path.abspath(DEFAULT_LOGGING_CONF_PATH)
