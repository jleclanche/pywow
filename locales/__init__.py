#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Import default language.
If need more dynamic logic, with code may be helpful:

import os
locale = os.environ.get('WDBC_LOCALE', 'en').lower()
L = getattr(__import__('wdbc.locales.' + locale, fromlist=['MESSAGES']), 'MESSAGES')
"""

from .en_US import MESSAGES as L

