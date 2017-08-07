# onderwijsnummer.py - functions for handling onderwijsnummers
#
# Copyright (C) 2012, 2013 Arthur de Jong
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301 USA

"""Onderwijsnummer (Dutch student school number).

The onderwijsnummers (education number) is very similar to the BSN (Dutch
national identification number) for students without a BSN. It uses a
checksum mechanism similar to the BSN.

>>> validate('1012.22.331')
'101222331'
>>> validate('100252333')
Traceback (most recent call last):
    ...
InvalidChecksum: ...
>>> validate('1012.22.3333')
Traceback (most recent call last):
    ...
InvalidLength: ...
>>> validate('2112.22.337')  # number must start with 10
Traceback (most recent call last):
    ...
InvalidFormat: ...
"""

from stdnum.exceptions import *
from stdnum.nl.bsn import compact, checksum


__all__ = ['compact', 'validate', 'is_valid']


def validate(number):
    """Checks to see if the number provided is a valid onderwijsnummer.
    This checks the length and whether the check digit is correct and
    whether it starts with the right sequence."""
    number = compact(number)
    if not number.isdigit() or int(number) <= 0:
        raise InvalidFormat()
    if not number.startswith('10'):
        raise InvalidFormat()
    if len(number) != 9:
        raise InvalidLength()
    if checksum(number) != 5:
        raise InvalidChecksum()
    return number


def is_valid(number):
    """Checks to see if the number provided is a valid onderwijsnummer.
    This checks the length and whether the check digit is correct and
    whether it starts with the right sequence."""
    try:
        return bool(validate(number))
    except ValidationError:
        return False