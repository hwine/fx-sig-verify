#!/usr/bin/env python

# Copyright 2012 Google Inc. All Rights Reserved.
#
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
#
# Author: caronni@google.com (Germano Caronni)

"""X.509 Time class and utility functions.

   Limited interpretation of ASN.1 time formats,
   as specified in RFC2459, section 4.1.2.5
"""

import calendar
import time


from pyasn1 import error
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1.type import useful


class Time(univ.Choice):
  componentType = namedtype.NamedTypes(
      namedtype.NamedType('utcTime', useful.UTCTime()),
      namedtype.NamedType('generalTime', useful.GeneralizedTime()))

  # pyasn1 0.3.1+ also supports .toDateTime() for ASN.1 time types
  def ToPythonEpochTime(self):
    """Takes a ASN.1 Time choice, and returns seconds since epoch in UTC."""
    if not self.hasValue():
        raise error.PyAsn1Error('Neither utcTime nor generalTime is present.')
    name = self.getName()
    component = self.getComponent()
    if component is None or not component.hasValue():
      raise error.PyAsn1Error('Neither utcTime nor generalTime is present.')
    if name == 'generalTime':
      format_str = '%Y%m%d%H%M%SZ'
      time_str = str(component)
    else:
      format_str = '%y%m%d%H%M%SZ'
      time_str = str(component)
    time_tpl = time.strptime(time_str, format_str)
    return calendar.timegm(time_tpl)
